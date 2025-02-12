from enum import Enum
from typing import Tuple

import numpy as np

from core.models.population import Individual

class CrossoverType(Enum):
    OX = 'ox'
    PMX = 'pmx'

def ordered_crossover(
        parent1: Individual,
        parent2: Individual,
    ) -> Tuple[Individual, Individual]:
    """
    Implementation of the Ordered Crossover algorithm
    :param parent1: Individual - the first parent
    :param parent2: Individual - the second parent
    :param seed: int - random seed
    :return: Tuple[Individual, Individual] - the two offspring
    """

    # Get the length of the chromosome
    assert len(parent1.path) == len(parent2.path), 'The length of the chromosomes should be the same'
    chromosome_length = len(parent1.path)

    # Initialize the child paths
    child1_path = np.full((chromosome_length,), -1, dtype=int)
    child2_path = np.full((chromosome_length,), -1, dtype=int)

    random_subset = np.random.randint(0, chromosome_length, 2)
    start, end = min(random_subset), max(random_subset)
    subset1 = parent1.path[start:end]
    subset2 = parent2.path[start:end]

    # Copy the subset to the child paths
    child1_path[start:end] = subset1
    child2_path[start:end] = subset2

    set1 = set(subset1)
    set2 = set(subset2)

    # Fill the remaining slots
    parent2_index = 0
    for i in range(chromosome_length):
        if child1_path[i] == -1:
            while parent2.path[parent2_index] in set1:
                parent2_index += 1
            child1_path[i] = parent2.path[parent2_index]
            parent2_index += 1

    parent1_index = 0
    for i in range(chromosome_length):
        if child2_path[i] == -1:
            while parent1.path[parent1_index] in set2:
                parent1_index += 1
            child2_path[i] = parent1.path[parent1_index]
            parent1_index += 1

    child1 = Individual(path=child1_path, distance=0, fitness=0)
    child2 = Individual(path=child2_path, distance=0, fitness=0)

    return child1, child2


def partial_mapped_crossover(
        parent1: Individual,
        parent2: Individual,
    ) -> Tuple[Individual, Individual]:
    """
    Implementation of the Partial Mapped Crossover algorithm

    Thanks to
    https://observablehq.com/@swissmanu/pmx-crossover
    for code inspiration

    :param parent1: List[int] - the first parent
    :param parent2: List[int] - the second parent
    :param seed: int - random seed
    :return: Tuple[Individual, Individual] - the two offspring
    """

    # Get the length of the chromosome
    assert len(parent1.path) == len(parent2.path), 'The length of the chromosomes should be the same'
    chromosome_length = len(parent1.path)

    random_subset = np.random.randint(0, chromosome_length, 2)
    start, end = min(random_subset), max(random_subset)

    child1_path = parent1.path[:]
    child2_path = parent2.path[:]
    mapping1 = {}
    mapping2 = {}

    # Map Slice:
    for i in range(start, end):
        mapping1[parent2.path[i]] = parent1.path[i]
        child1_path[i] = parent2.path[i]

        mapping2[parent1.path[i]] = parent2.path[i]
        child2_path[i] = parent1.path[i]

    # Repair Lower Slice:
    for i in range(start):
        while child1_path[i] in mapping1:
            child1_path[i] = mapping1[child1_path[i]]
        while child2_path[i] in mapping2:
            child2_path[i] = mapping2[child2_path[i]]

    # Repair Upper Slice:
    for i in range(end, len(child1_path)):
        while child1_path[i] in mapping1:
            child1_path[i] = mapping1[child1_path[i]]
        while child2_path[i] in mapping2:
            child2_path[i] = mapping2[child2_path[i]]

    child1 = Individual(path=child1_path, distance=0, fitness=0)
    child2 = Individual(path=child2_path, distance=0, fitness=0)

    return child1, child2
