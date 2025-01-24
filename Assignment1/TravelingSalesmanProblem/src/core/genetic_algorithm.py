from datetime import datetime
import random
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt

from parsers.tsp_parser import load_tsp_file
from utils.common import (
    generate_distance_matrix,
    calculate_total_distance,
    calculate_total_distance_for_population
)
from core.evaluation.fitness import calculate_fitness_of_population, calculate_fitness
from core.selection.selection_algorithm import tournament_selection, roulette_wheel_selection
from core.crossover.crossover_alogrithm import ordered_crossover, partial_mapped_crossover
from core.mutation.mutation_algorithm import swap_mutation, scramble_mutation, inversion_mutation

"""

Genetic Algorithm

1. Initialize population
2. Evaluate fitness of each individual

"""


def generate_population(population_size: int, dimension: int) -> List[List[int]]:
    """
    Geerate a population of individuals
    :param population_size: int - the amount of individuals in the population
    :param dimension: int - the number of cities
    :return: List[List[int]] - a list of individuals
    """

    population = []
    while len(population) < population_size:
        individual = list(range(dimension))
        np.random.shuffle(individual)
        if individual not in population:
            population.append(individual)

    return population



"""
Steps
1. Generate a random population
2. Evaluate the fitness of each individual in the population
3. Selectection step
4. Perform crossover on the selected individuals
5. Perform mutation on the offspring
6. Reevaluate the fitness of the offspring
"""


def main():
    population_size = 1_000
    file_path = 'tsp/berlin52.tsp'
    problem = load_tsp_file(file_path)

    x_coords = [city[0] for city in problem['cities']]
    y_coords = [city[1] for city in problem['cities']]

    plt.scatter(x_coords, y_coords, c='blue', marker='o')
    plt.grid(True)
    plt.show()


    distance_matrix: np.ndarray = generate_distance_matrix(problem['dimensions'], problem['cities'])


    # step 1: generate a random population
    population = generate_population(
        population_size=population_size,
        dimension=problem['dimensions']
    )

    best_individuals = []
    best_ever = None

    for i in range(5_000):
        # step 2: evaluate the fitness of the population
        total_distances = calculate_total_distance_for_population(population, distance_matrix)
        population_fitness = calculate_fitness_of_population(total_distances)

        # step 3: selection step, for the elite
        top_individuals = tournament_selection(
            population_fitness=population_fitness,
            selects=population_size // 2,
            tournament_size=2
        )

        # print(f'Top individuals: {top_individuals}\n')

        # step 4: perform crossover on the selected individuals
        offspring = []
        for individual in range(0, len(top_individuals), 2):
            parent1 = population[top_individuals[individual]]
            parent2 = population[top_individuals[individual + 1]]

            if random.randint(0, 2) == 0:
                child1, child2 = partial_mapped_crossover(parent1, parent2)

                offspring.append(child1)
                offspring.append(child2)

        # step 5: perform mutation on the offspring
        for child in offspring:
            if random.randint(0, 5) == 1:
                child = swap_mutation(child)

        # step 6: reevaluate the fitness of the offspring
        total_distances_offspring = calculate_total_distance_for_population(offspring, distance_matrix)
        offspring_fitness = calculate_fitness_of_population(total_distances_offspring)

        # step 7: create a new population

        combined_population = population + offspring
        combined_fitness = population_fitness + offspring_fitness
        

        top_individuals = tournament_selection(
            population_fitness=combined_fitness,
            selects=population_size // 2,
            tournament_size=2
        )

        new_population = [combined_population[top] for top in top_individuals]

        # fill the rest of the population with random individuals
        while len(new_population) < population_size:
            individual = list(range(problem['dimensions']))
            np.random.shuffle(individual)
            if individual not in new_population:
                new_population.append(individual)

        population = new_population

        # print out best individual in this generation
        total_distances = calculate_total_distance_for_population(population, distance_matrix)
        new_population_fitness = calculate_fitness_of_population(total_distances)
        best_individual = np.argmax(new_population_fitness)
        # print(f'Generation {i} - Best individual: {best_individual} - followed the following cities: {population[best_individual]}\n')
        # print(f'Distance of best individual: {total_distances[best_individual]}\n\n')
        print(f'finished generation {i+1}')
        best_individuals.append(total_distances[best_individual])


    print(f'Best distance for individual: {best_individuals[-1]}')
    print(f'Best fitness for individual {calculate_fitness(best_individuals[-1])}')

    best_ever = np.argmin(best_individuals)
    print(f'Best ever distance: {best_individuals[best_ever]}')

    plt.plot(best_individuals)
    plt.xlabel('Generation')
    plt.ylabel('Distance')
    plt.title('Distance of best individual per generation')
    plt.show()

def plot_path(path: List[int], cities: List[Tuple[float, float]]):
    x_coords = [cities[i][0] for i in path]
    y_coords = [cities[i][1] for i in path]

    x_coords.append(cities[path[0]][0])
    y_coords.append(cities[path[0]][1])

    plt.scatter(x_coords, y_coords, c='blue', marker='o')

    plt.plot(x_coords, y_coords, c='red')

    plt.title('Best path')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.grid(True)
    plt.show()

def run(
        population_size: int = 1_000,
        generations: int = 10_000,
        chance_of_crossover: int = 95,
        chance_of_mutation: int = 15,
        file_path: str = 'tsp/berlin52.tsp'
    ):

    problem = load_tsp_file(file_path)

    # 2d array of city distances, where the index defines the city
    distance_matrix: np.ndarray = generate_distance_matrix(problem['dimensions'], problem['cities'])

    # generate a random population with no duplicates
    random_population = generate_population(
        population_size=population_size,
        dimension=problem['dimensions']
    )

    all_population_fitnesses = []
    all_population_distance = []

    # Loop through the generations
    for i in range(generations):

        print(f'Generation {i+1}')

        # step 2. Evaluate the fitness of each individual in the population
        # First we need to calculate the total distance of each individual in the population
        population_total_distance = calculate_total_distance_for_population(random_population, distance_matrix)

        _best_individual_path = np.argmin(population_total_distance)
        all_population_distance.append(calculate_total_distance(random_population[_best_individual_path], distance_matrix))

        # Then we calculate the fitness of each individual, which is the inverse of the distance
        population_fitness = calculate_fitness_of_population(population_total_distance)
        all_population_fitnesses.append(np.argmax(population_fitness))

        # step 3. Selection step for the 'elite'.
        # This step doesn't necessarily pick the best individuals, but the best individuals have a higher chance of being selected
        top_individuals_index = tournament_selection(
            population_fitness=population_fitness,
            selects=population_size // 2,
            tournament_size=3
        )

        # step 4. Perform crossover on the 'elite' / selected individuals
        offspring_paths = []
        for individual in range(0, len(top_individuals_index), 2):
            parent1_path = random_population[top_individuals_index[individual]]
            parent2_path = random_population[top_individuals_index[individual + 1]]

            if random.randint(0, 100) < chance_of_crossover:
                child1_path, child2_path = partial_mapped_crossover(parent1_path, parent2_path)

                offspring_paths.append(child1_path)
                offspring_paths.append(child2_path)

        # step 5. Perform mutation on the offspring
        for child_path in offspring_paths:
            if random.randint(0, 100) < chance_of_mutation:
                child_path = swap_mutation(child_path)

        # step 6. Reevaluate the fitness of the offspring
        offspring_total_distance = calculate_total_distance_for_population(offspring_paths, distance_matrix)
        offspring_fitness = calculate_fitness_of_population(offspring_total_distance)

        # step 7. Create a new population
        combined_population = random_population + offspring_paths # list of paths
        combined_fitness = population_fitness + offspring_fitness # list of fitness

        top_individuals_index = tournament_selection(
            population_fitness=combined_fitness,
            selects=population_size // 2,
            tournament_size=7
        )

        new_population = [combined_population[top] for top in top_individuals_index] # list of paths

        # fill the rest of the population with random individuals
        while len(new_population) < population_size:
            individual = list(range(problem['dimensions']))
            np.random.shuffle(individual)
            if individual not in new_population:
                new_population.append(individual)
        random_population = new_population


    # calculate the total distance of the best individual
    distance_for_last_generation_population = calculate_total_distance_for_population(random_population, distance_matrix)
    best_individual_path = np.argmin(distance_for_last_generation_population)
    plot_path(random_population[best_individual_path], problem['cities'])

    print(f'Distance: {calculate_total_distance(random_population[best_individual_path], distance_matrix)}')

    plt.plot(all_population_fitnesses)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness of best individual per generation')
    plt.show()

    plt.plot(all_population_distance)
    plt.xlabel('Generation')
    plt.ylabel('Distance')
    plt.title('Distance of best individual per generation')
    plt.show()
