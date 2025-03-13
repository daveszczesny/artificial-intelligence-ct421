import copy
import random
from typing import List

import numpy as np

from core.models.agent import Agent
from core.models.action import Action
from core.utils.generate import generate_agents
from core.utils import plot
from core.selection.selection_algorithm import tournament_selection
from core.crossover.crossover_algorithm import single_point_cx
from core.mutation.mutation_algorithm import scramble_mutation, swap_mutation
from core.strategy.strategy import Strategy

from core.idp import update_scores
from core.idp import play as play_vs_strategy

def count_actions(agents_actions):
    # count the number of cooperations and defections
    cooperation_count = agents_actions.count(Action.COOPERATE)
    defection_count = agents_actions.count(Action.DEFECT)
    return cooperation_count, defection_count

def get_payoff(agent_action: Action, cooperation_count: int, defection_count: int):
    """
    Function to calculate the payoff for an agent based on their action,
    The payoff is calculated by the given formula
    if the agent cooperates, their payoff could be:
    Payoff = 3 * C - 1 * D
    if the agent defects, their payoff could be:
    Payoff = 5 * C - 2 * D
    :param agent_action: Action
    :param cooperation_count: int
    :param defection_count: int
    :return payoff: int - the payoff for the agent
    """
    if agent_action == Action.COOPERATE:
        return (2 * cooperation_count) - (2 * defection_count)
    else:
        return (6 * cooperation_count) - (1 * defection_count)

def play_agent_vs_agent(agent_1: Agent, agent_2: Agent):
    agent_1 = copy.deepcopy(agent_1)
    agent_2 = copy.deepcopy(agent_2)
    
    agent1_score,agent2_score = 0, 0

    for _ in range(len(agent_1.strategy)):
        agent1_action = agent_1.next_action()
        agent2_action = agent_2.next_action()
        agent1_score, agent2_score = update_scores(
            agent1_action,
            agent2_action,
            agent1_score,
            agent2_score
        )

    return agent1_score, agent2_score

def play_game(agents: List[Agent]):
    agents = [copy.deepcopy(agent) for agent in agents]

    scores = [0 for _ in agents]

    for _ in range(len(agents[0].strategy)):
        agents_actions = [agent.next_action() for agent in agents]

        cooperation_count, defection_count = count_actions(agents_actions)

        for i in range(len(agents)):
            scores[i] += get_payoff(agents_actions[i], cooperation_count, defection_count)
    
    # mean the scores
    scores = [score / len(agents) for score in scores]

    return scores


def calculate_fitness(agent_clusters: List[List[Agent]], rounds_per_game: int = 100, sample_size: int = 10):
    """
    Calculate the fitness of agents in the cluster
    In order to reduce the complexity the function will randomly sample a subset of the agents
    and play them against each other
    :param agent_cluster: List[List[Agent]]
    :param rounds_per_game: int
    :param sample_size: int
    """

    # reset the fitness of all agents
    for cluster in agent_clusters:
        for agent in cluster:
            agent.fitness = 0

    # play the agents against each other
    for i in range(len(agent_clusters)):
        for j in range(i + 1, len(agent_clusters)):
            combined_agents = agent_clusters[i] + agent_clusters[j]
            scores = play_game(combined_agents)

            for k, agent in enumerate(agent_clusters[i]):
                agent.fitness += scores[k]
            for k, agent in enumerate(agent_clusters[j]):
                agent.fitness += scores[k + len(agent_clusters[i])]

    # normalise the fitness and play the agents against a random fixed strategy
    total_agents = sum(len(cluster) for cluster in agent_clusters)
    for cluster in agent_clusters:
        for agent in cluster:
            agent.fitness /= total_agents
            for strat in list(Strategy):
                agent.fitness += play_vs_strategy(
                    agent.strategy,
                    strat,
                    100
                )


    return agent_clusters

def calculate_population_fitness(agents, other_agents, rounds_per_game: int = 100):
    for agent in agents:
        agent.fitness = 0

    for agent in agents:
        fitness = 0
        for other_agent in other_agents:
            fitness += play_game([agent, other_agent])[0]
        agent.fitness = fitness / len(other_agents)
    return agents

def main(
        generations: int = 500,
        rounds_per_game: int = 100,
        number_of_agents: int = 5,
        elite_size: int = 3
):
    # to have n agents we need to loop the generate_agents function n times
    agent_cluster: List[List[Agent]] = [generate_agents(10, rounds_per_game) for _ in range(number_of_agents)]

    # calculate initial fitness by playing all agents against each other
    agent_cluster = calculate_fitness(agent_cluster, rounds_per_game)

    agent_cluster_fitness_tracker: List[List[int]] = [[] for _ in range(number_of_agents)]
    total_cooperation_tracker: List[List[float]] = [[] for _ in range(generations)]
    total_defection_tracker: List[List[float]] = [[] for _ in range(generations)]

    offsprings_generated = [[] for _ in range(number_of_agents)]

    for gen in range(generations):
        offsprings_generated = [[] for _ in range(number_of_agents)] # reset offspring
        print(f'Generation: {gen}')
        elite_agents_list: List[List[Agent]] = [cluster[:elite_size] for cluster in agent_cluster]

        # count the total number of cooperations in every agent across every cluster

        """
        I want to get the average cooperation and defection across all agents in all clusters per generation
        So that the average cooperation and defection can be plotted
        """

        cooperation_count, defection_count = 0, 0
        for cluster in agent_cluster:
            for agent in cluster:
                cooperation_count += agent.strategy.count(Action.COOPERATE)
                defection_count += agent.strategy.count(Action.DEFECT)
        total_cooperation_tracker[gen] = cooperation_count
        total_defection_tracker[gen] = defection_count


        # tournament selection
        for cluster in agent_cluster:
            selected_agents = tournament_selection(
                agents=cluster,
                selects=int(len(cluster) * 0.8),
                tournament_size=3
            )

            # crossover
            offspring = []
            random.shuffle(selected_agents)

            for i in range(0, len(selected_agents), 2):
                if i + 1 >= len(selected_agents):
                    offspring.append(selected_agents[i])
                    break
                
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

                # add all the offsprings to the global offspring list
                offsprings_generated[agent_cluster.index(cluster)].append(agent)

            # this is wrong we need to escape the forloop here

        # loop through all the offsprings generated from the previous loop and calculate their fitness
        for i, offspring_cluster in enumerate(offsprings_generated):
            if i+1 >= len(offsprings_generated):
                offsprings_generated[i] = calculate_population_fitness(
                    agents = offspring_cluster,
                    other_agents = offsprings_generated[0],
                    rounds_per_game=rounds_per_game
                )
            else:
                offsprings_generated[i] = calculate_population_fitness(
                    agents = offspring_cluster,
                    other_agents = offsprings_generated[i+1],
                    rounds_per_game=rounds_per_game
                )

            # have the offsprings also play against fixed strategies
            for offspring in offspring_cluster:
                for strat in list(Strategy):
                    offspring.fitness += play_vs_strategy(
                        offspring.strategy,
                        strat,
                        rounds_per_game
                    )


        for cluster in agent_cluster:
            offspring = offsprings_generated[agent_cluster.index(cluster)]

            for index, child in enumerate(offspring):
                if tuple(child.strategy) in [tuple(agent.strategy) for agent in cluster]:
                    continue
                cluster[-(index+1)] = child
            cluster[:elite_size] = elite_agents_list[agent_cluster.index(cluster)]

            cluster.sort(key=lambda x: x.fitness, reverse=True)

        # sort the clusters based on the fitness of the agents
        agent_cluster.sort(key=lambda x: x[0].fitness, reverse=True)

        for i, cluster in enumerate(agent_cluster):
            agent_cluster_fitness_tracker[i].append(cluster[0].fitness)

    # play two of the best clusters against each other

    best_agent_1 = agent_cluster[0][0]
    best_agent_2 = agent_cluster[1][0]

    scores = play_agent_vs_agent(best_agent_1, best_agent_2)
    print(f'Best agent 1 scored: {scores[0]}, Best agent 2 scored: {scores[1]}')

    for index, cluster in enumerate(agent_cluster):
        print(f'Cluster {index+1} against fixed strategies')
        scores = {
            "Always Cooperate: ":  play_vs_strategy(cluster[0].strategy, Strategy.ALWAYS_COOPERATE, rounds_per_game),
            "Always Defect: ": play_vs_strategy(cluster[0].strategy, Strategy.ALWAYS_DEFECT, rounds_per_game),
            "TFT: ": play_vs_strategy(cluster[0].strategy, Strategy.TIT_FOR_TAT, rounds_per_game),
            "Grim Trigger: ": play_vs_strategy(cluster[0].strategy, Strategy.GRIM_TRIGGER, rounds_per_game),
            "Pavlov: ": play_vs_strategy(cluster[0].strategy, Strategy.PAVLOV, rounds_per_game)
        }

        for key, value in scores.items():
            print(f"in {key} scored: {value}")


    plot.plot_multi_agents_fitness_over_time(agent_cluster_fitness_tracker)
    plot.plot_multi_agents_cooperation_and_defect_over_time(total_cooperation_tracker, total_defection_tracker)

    for index, cluster in enumerate(agent_cluster):
        plot.plot_cooperation_versus_defect(cluster[0].strategy, cluster=index+1)
