from datetime import datetime

import numpy as np

from parsers.tsp_parser import load_tsp_file
from utils.common import generate_distance_matrix, calculate_total_distance, calculate_total_distance_for_population
from core.genetic_algorithm import generate_population
from core.evaluation.fitness import calculate_fitness_of_population
from core.selection.selection_algorithm import roulette_wheel_selection, tournament_selection
from core.crossover.crossover_alogrithm import ordered_crossover, partial_mapped_crossover
from core.mutation.mutation_algorithm import swap_mutation, scramble_mutation
from core import genetic_algorithm

# file_path = 'tsp/berlin52.tsp'
# start_time = datetime.now()
# problem = load_tsp_file(file_path)

# distance_matrix: np.ndarray = generate_distance_matrix(problem['dimensions'], problem['cities'])


# population = generate_population(
#     population_size=10,
#     dimension=problem['dimensions'])
# # print(population[0])

# total_distance = calculate_total_distance(population[0], distance_matrix)
# # print('%.2f' % total_distance)

# total_distances = calculate_total_distance_for_population(population, distance_matrix)

# population_fitness = calculate_fitness_of_population(total_distances)
# for i, fitness in enumerate(population_fitness):
#     print(f'Individual {i} fitness: {fitness}')


# # getting top 3 individuals based on fitness
# top_individuals = np.argsort(population_fitness)[:3]
# print(top_individuals)
# for i in top_individuals:
#     print(f'Individual {i} fitness: {population_fitness[i]}')


# selected_individuals_roulette = roulette_wheel_selection(population_fitness, selects=2)
# print('\nroulette')
# for i in selected_individuals_roulette:
#     print(f'Selected individual {i} fitness: {population_fitness[i]}')

# selected_individuals_tournament = tournament_selection(population_fitness, selects=2, tournament_size=3)
# print('\ntournament')
# for i in selected_individuals_tournament:
#     print(f'Selected individual {i} fitness: {population_fitness[i]}')

# # crossover
# parent1 = population[selected_individuals_roulette[0]]
# parent2 = population[selected_individuals_roulette[1]]
# child1, child2 = ordered_crossover(parent1, parent2)
# print('\nCrossover (OX)')
# print('Parent 1:', parent1)
# print('Parent 2:', parent2)
# # print('Child 1:', child1)
# # print('Child 2:', child2)

# child3, child4 = partial_mapped_crossover(parent1, parent2)
# print('\nCrossover (pmx)')
# print('Child 3:', child3)
# # print('Child 4:', child4)

# total_distance_child3 = calculate_total_distance(child3, distance_matrix)

# child5 = swap_mutation(child3)
# print('\nMutation (scramble)')
# print('Child 5:', child5)
# total_distance_child5 = calculate_total_distance(child5, distance_matrix)

# print(f'\nTotal distance child 3: {total_distance_child3}')
# print(f'Total distance child 5: {total_distance_child5}')



genetic_algorithm.run()