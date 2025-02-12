import random
from typing import Optional, List

import numpy as np

from core.models.population import Population, Individual
from core.evaluation.fitness import calculate_fitness
from core.evaluation.distance import calculate_total_distance

def generate_initial_population(
        population_size: int,
        dimensions: int,
        distance_matrix: np.ndarray,
        individuals: Optional[List[Individual]] = None
    ) -> Population:

    """
    Generate a random population with unique paths.
    Calculate the distance and fitness for each of these individuals
    """

    if individuals is None:
        individuals = []
    unique_paths = set(tuple(ind.path) for ind in individuals)

    generated_individuals = 0

    while len(individuals) < population_size:
        individual = Individual(
            path=random.sample(range(dimensions), dimensions),
            distance=0,
            fitness=0
        )

        individual.distance = calculate_total_distance(individual.path, distance_matrix)
        individual.fitness = calculate_fitness(individual.distance)

        # we need to check if the individual with that path already exists
        # if it does, we skip it
        if tuple(individual.path) not in unique_paths:
            individuals.append(individual)
            generated_individuals += 1
            unique_paths.add(tuple(individual.path))

    print(f'Generated {generated_individuals} unique individuals')
    return Population(individuals=individuals)
