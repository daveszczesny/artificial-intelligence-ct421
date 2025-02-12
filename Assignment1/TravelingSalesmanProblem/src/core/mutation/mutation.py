from enum import Enum
from typing import Dict, List
import random
import numpy as np

from core.mutation.mutation_algorithm import swap_mutation, inversion_mutation, scramble_mutation
from core.evaluation.distance import calculate_total_distance
from core.evaluation.fitness import calculate_fitness
from core.models.population import Individual

class MutationType(Enum):
    SWAP = 'swap'
    SCRAMBLE = 'scramble'
    INVERSION = 'inversion'

def apply_mutation(
        offspring: List[Individual],
        mutation_type: Dict[MutationType ,int],
        chance_of_mutation: int,
        distance_matrix: np.ndarray
    ) -> List[Individual]:
    """
    Apply mutation to the offspring
    :param offspring: List[Individual] - the offspring to mutate
    :param mutation_type: Dict[MutationType, int] - the mutation type and their probabilities
    :param chance_of_mutation: int - the chance of mutation
    :param distance_matrix: np.ndarray - the distance matrix
    :return: List[Individual] - the mutated offspring
    """

    total = sum(mutation_type.values())
    mutation_probabilities = [value / total for value in mutation_type.values()]

    for index, individual in enumerate(offspring):

        if random.randint(0, 100) < chance_of_mutation:
            mutation = np.random.choice(list(mutation_type.keys()), size=1, p=mutation_probabilities)[0]

            if mutation == MutationType.SWAP:
                offspring[index] = swap_mutation(individual)
            elif mutation == MutationType.INVERSION:
                offspring[index] = inversion_mutation(individual)
            elif mutation == MutationType.SCRAMBLE:
                offspring[index] = scramble_mutation(individual)

        offspring[index].distance = calculate_total_distance(offspring[index].path, distance_matrix)
        offspring[index].fitness = calculate_fitness(offspring[index].distance)

    return offspring
