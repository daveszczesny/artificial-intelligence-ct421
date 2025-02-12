import time
import random
from typing import List, Dict, Any
import copy
import numpy as np

from parsers.tsp_parser import load_tsp_file
from utils.plotting import plot_distance_over_time, plot_fitness_over_time, plot_path
from utils.common import np_to_python, write_to_json
from utils.generate import generate_initial_population
from core.evaluation.distance import generate_distance_matrix
from core.selection.selection_algorithm import tournament_selection, roulette_wheel_selection
from core.crossover.crossover_alogrithm import ordered_crossover, partial_mapped_crossover, CrossoverType
from core.mutation.mutation import apply_mutation, MutationType
from core.models.population import Population, Individual


"""
Steps
1. Generate a random population
2. Evaluate the fitness of each individual in the population
3. Selectection step
4. Perform crossover on the selected individuals
5. Perform mutation on the offspring
6. Construct a new population
"""

def run(
        population_size: int = 100,
        generations: int = 1_000,
        chance_of_crossover: int = 95,
        chance_of_mutation: int = 6,
        elites_size: int = 5,
        file_path: str = 'tsp/berlin52.tsp',
        verbose: int = 0,
        early_stop: int = 1000,
        crossover_type: Dict[CrossoverType, int] = {
            CrossoverType.OX: 50, CrossoverType.PMX: 50
            },
        selection_type: str = 'tournament',
        mutation_type: Dict[MutationType, int] = {
            MutationType.SWAP: 50,
            MutationType.SCRAMBLE: 25,
            MutationType.INVERSION: 25
        },
        write_results: bool = False,
        plot_graphs: bool = False
    ):

    assert selection_type in ['tournament', 'roulette'], 'Invalid selection type'
    assert sum(crossover_type.values()) == 100, 'Crossover type values must add up to 100'
    assert sum(mutation_type.values()) == 100, 'Mutation type values must add up to 100'

    start_time = time.time()

    problem = load_tsp_file(file_path)

    # 2d array of city distances, where the index defines the city
    distance_matrix: np.ndarray = generate_distance_matrix(problem['dimensions'], problem['cities'])

    # Generate the initial population
    population: Population = generate_initial_population(
        population_size=population_size,
        dimensions=problem['dimensions'],
        distance_matrix=distance_matrix
    )

    # sort the population by distance, from shortest to longest
    population.individuals.sort(key=lambda x: x.distance, reverse=False)

    early_stoppage = {
        'counter': 0,
        'individual': population.individuals[0]
    }

    tracker: List[Dict[str, Any]] = []
    generation_tracker: Dict[str, Any] = {}

    # Selection Step
    for g in range(generations):
        
        if 'generation' in generation_tracker:
            if generation_tracker['best_distance'] == population.individuals[0].distance:
                pass
            else:
                generation_tracker['generation'] = g+1
                generation_tracker['best_fitness'] = population.individuals[0].fitness
                generation_tracker['best_distance'] = population.individuals[0].distance
                generation_tracker['average_distance'] = np.mean([ind.distance for ind in population.individuals])
                tracker.append(generation_tracker)

        generation_tracker = {
            'generation': g+1,
            'best_fitness': population.individuals[0].fitness,
            'best_distance': population.individuals[0].distance,
            'average_distance': np.mean([ind.distance for ind in population.individuals]),
        }

        if verbose > 0: print(f'Population size: {len(population.individuals)}')

        elites = copy.deepcopy(population.individuals[:elites_size]) # get the best individuals

        if elites[0].distance == early_stoppage['individual'].distance:
            early_stoppage['counter'] += 1
        else:
            early_stoppage['counter'] = 0
            early_stoppage['individual'] = population.individuals[0]

        if early_stoppage['counter'] > early_stop:
            print(f'Early stopping at generation {g}')
            break

        no_selects_parents = int( len(population.individuals) * 0.8)
        
        if selection_type == 'roulette':
            parents: List[Individual] = roulette_wheel_selection(
                population=population,
                selects=int(no_selects_parents)
            )
        else: # tournament
            parents: List[Individual] = tournament_selection(
                population=population,
                selects=int(no_selects_parents),
                tournament_size=3
            )

        if verbose > 0: print(f'Parents selected: {len(parents)}')

        # Perform crossover on the parents to create new offspring `Individuals`
        offspring: List[Individual] = []
        random.shuffle(parents) # shuffle the parents to avoid bias

        for i in range(0, len(parents), 2):
            if i + 1 >= len(parents):
                    # if we have an odd number of parents, we just add the last parent to the offspring
                    offspring.append(parents[i])
                    break

            # Perform crossover
            if random.randint(0, 100) < chance_of_crossover:
                if CrossoverType.OX in crossover_type and CrossoverType.PMX in crossover_type:
                    crossover_type_chance = random.randint(0, 100)
                    if crossover_type_chance < crossover_type[CrossoverType.OX]:
                        child1, child2 = ordered_crossover(parents[i], parents[i+1])
                    else:
                        child1, child2 = partial_mapped_crossover(parents[i], parents[i+1])
                elif CrossoverType.OX in crossover_type:
                    child1, child2 = ordered_crossover(parents[i], parents[i+1])
                else: # PMX
                    child1, child2 = partial_mapped_crossover(parents[i], parents[i+1])

                offspring.append(child1)
                offspring.append(child2)
            else:
                # if no crossover is performed, we just add the parents to the offspring
                offspring.append(parents[i])
                offspring.append(parents[i+1])



        offspring = apply_mutation(offspring, mutation_type, chance_of_mutation, distance_matrix)


        # replace the worst individuals with the offspring
        for i in range(0, len(offspring)):
            if tuple(offspring[i].path) in set(tuple(ind.path) for ind in population.individuals):
                # if the path already exists, we skip it
                continue
            # replace the worst individuals with the offspring
            population.individuals[-(i+1)] = offspring[i]

        population.individuals[0:elites_size] = elites

        # sort again
        population.individuals.sort(key=lambda x: x.distance, reverse=False)

        average_distance = sum([individual.distance for individual in population.individuals]) / len(population.individuals)
        print(f'Generation: {g}, '
              f'Best fitness: {population.individuals[0].fitness}, '
              f'Best distance: {population.individuals[0].distance:.2f}, '
              f'Avg. Distance: {average_distance:.2f}')


    end_time = time.time()
    time_taken = end_time - start_time

    if plot_graphs:
        plot_path(path=population.individuals[0].path, cities=problem['cities'])
        plot_fitness_over_time(tracker)
        plot_distance_over_time(tracker)

    run_tracker = {
        'highlights': tracker,
        'best_individual': population.individuals[0].to_dict(),
        'time_taken': time_taken,
        'options': {
            'generations': generations,
            'population_size': population_size,
            'early_stop': early_stop,
            'chance_of_mutation': chance_of_mutation,
            'chance_of_crossover': chance_of_crossover,
            'selection_type': selection_type,
            'crossover_type': {
                k.name: v for k, v in crossover_type.items()
            },
            'mutation_type': {
                k.name: v for k, v in mutation_type.items()
            },
            'file_path': file_path,
            'elites_size': elites_size,
            'verbose': verbose,
        }
    }


    run_tracker = np_to_python(run_tracker)

    if write_results:
        file_name = f'results_{file_path.split("/")[1].split(".")[0]}.json'
        write_to_json(run_tracker, file_name)

    return {
        'best_individual': population.individuals[0].to_dict(),
        'time_taken': time_taken,
    }
