
"""
Game rules
1. Two players play the game. They each get to choose an action (either cooperate or defect).
2. If both players cooperate, they each get 3 points.
3. If both players defect, they each get 1 point.
4. If one player cooperates and the other defects, the cooperator gets 0 points and the defector gets 5 points.
"""
import random
import copy

import numpy as np

from core.models.agent import Agent
from core.models.action import Action
from core.utils.generate import generate_from_strategy, generate_random_strategy, generate_agents
from core.utils import plot
from core.strategy.strategy import Strategy, get_strategy
from core.selection.selection_algorithm import tournament_selection
from core.crossover.crossover_algorithm import single_point_cx
from core.mutation.mutation_algorithm import scramble_mutation, swap_mutation

PAYOFF = {
    (1,1): (3, 3), # both agents cooperate
    (1,0): (0, 5), # agent 2 defects
    (0,1): (5, 0), # agent 1 defects
    (0,0): (1, 1), # both agents defect
}

def update_scores(agent1_action, agent2_action, agent1_score, agent2_score):
    payoff = PAYOFF[(agent1_action.value, agent2_action.value)]
    agent1_score += payoff[0]
    agent2_score += payoff[1]

    return agent1_score, agent2_score

def play_game(agent1: Agent, agent2: Agent):
    agent1 = copy.deepcopy(agent1)
    agent1_score = 0
    agent2_score = 0

    for _ in range(len(agent1.strategy)): # rounds of game
        agent1_action = agent1.next_action()
        agent2_action = agent2.next_action()
        agent1_score, agent2_score = update_scores(agent1_action, agent2_action, agent1_score, agent2_score)

    return agent1_score, agent2_score

def play(agent1_strategy: list = None, agent2_strat: Strategy = Strategy.ALWAYS_COOPERATE, rounds_per_game: int = 100) -> int:
    if agent1_strategy is None:
        agent1_strategy = generate_random_strategy(rounds_per_game)

    agent2_strategy = generate_from_strategy(rounds_per_game, agent2_strat, agent1_strategy)

    agent1 = Agent(agent1_strategy)
    agent2 = Agent(agent2_strategy)

    agent1_score, _ = play_game(agent1, agent2)

    return agent1_score

def calculate_fitness(agents, other_strategy: Strategy, rounds_per_game: int = 100):
    for agent in agents:
            agent.fitness = play(agent.strategy, other_strategy, rounds_per_game)
    return agents


def foo(strategy: Strategy = Strategy.PAVLOV):
    generations = 80
    rounds_per_game = 100

    population = generate_agents(50, rounds_per_game)
    elite_size = 3
    population = calculate_fitness(population, strategy, rounds_per_game)
    population.sort(key=lambda x: x.fitness, reverse=True)

    fitness_tracker = []
    strategy_tracker = []
    plot.plot_strategy_versus_other(
        population[0].strategy,
        get_strategy(strategy, rounds_per_game, population[0].strategy)
    )
    for gen in range(generations):
        
        fitness_tracker.append(population[0].fitness)
        # if gen % 10 == 0:
        #     print(f'Generation: {gen}, Current best strategy: {population[0].print_strategy()}')

        elite_agents = population[:elite_size]
        # tournament selection
        selected_agents = tournament_selection(
            agents=population,
            selects=int(len(population) * 0.8),
            tournament_size=3,
        )

        # crossover
        offspring = []
        random.shuffle(selected_agents)

        for i in range(0, len(selected_agents), 2):
            if i + 1 >= len(selected_agents):
                offspring.append(selected_agents[i])
                break

            # perform crossover
            if random.randint(0, 100) < 95: # chance at crossover
                child1, child2 = single_point_cx(
                    selected_agents[i].strategy,
                    selected_agents[i + 1].strategy
                )

                offspring.append(Agent(child1))
                offspring.append(Agent(child2))

            # perform mutation
            for index, agent in enumerate(offspring):
                if random.randint(0, 100) < 15:
                    if random.randint(0, 100) < 50:
                        offspring[index].strategy = scramble_mutation(agent.strategy)
                    else:
                        offspring[index].strategy = swap_mutation(agent.strategy)


        offspring = calculate_fitness(offspring, strategy, rounds_per_game)

        for index, offspring_agent in enumerate(offspring):
            if tuple(offspring_agent.strategy) in [tuple(agent.strategy) for agent in population]:
                continue
            population[-(index+1)] = offspring_agent

        population[0:elite_size] = elite_agents

        # sort again
        population.sort(key=lambda x: x.fitness, reverse=True)

        average_fitness = np.mean([agent.fitness for agent in population])
        print(f'Generation: {gen+1}, Best Fitness: {population[0].fitness}, Average Fitness: {average_fitness}')
        strategy_tracker.append(population[0].strategy)

    print(f'Best strategy: {population[0].print_strategy()}')
    plot.plot_fitness_over_time(fitness_tracker)
    plot.plot_cooperation_versus_defect(population[0].strategy)
    plot.plot_cooperation_and_defect_over_time(strategy_tracker)
    plot.plot_strategy_versus_other(
        population[0].strategy,
        get_strategy(strategy, rounds_per_game, population[0].strategy)
    )