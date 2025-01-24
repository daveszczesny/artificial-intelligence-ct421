from typing import List, Dict, Tuple

import numpy as np

def ordered_crossover(
        parent1: List[int],
        parent2: List[int],
        seed: int = 42,
    ) -> Tuple[List[int], List[int]]:
    """
    Implementation of the Ordered Crossover algorithm
    :param parent1: List[int] - the first parent chromosome
    :param parent2: List[int] - the second parent chromosome
    :param seed: int - random seed
    :return: Tuple[List[int], List[int]] - the two child chromosomes
    """

    np.random.seed(seed)

    # Get the length of the chromosome
    assert len(parent1) == len(parent2), 'The length of the chromosomes should be the same'
    chromosome_length = len(parent1)

    # Initialize the child chromosomes
    child1 = np.full((chromosome_length,), -1, dtype=int)
    child2 = np.full((chromosome_length,), -1, dtype=int)

    random_subset = np.random.randint(0, chromosome_length, 2)
    start, end = min(random_subset), max(random_subset)
    subset1 = parent1[start:end]
    subset2 = parent2[start:end]

    # Copy the subset from parent 1 to child1 and from parent 2 to child2
    child1[start:end] = subset1
    child2[start:end] = subset2

    # Copy the remaining elements from parent 2 to the child1
    parent2_index = 0
    for _ in range(chromosome_length):
        if parent2[parent2_index] not in subset1:
            for j in range(chromosome_length):
                if child1[j] == -1:
                    child1[j] = parent2[parent2_index]
                    parent2_index += 1
                    break
        else:
            parent2_index += 1

    # Copy the remaining elements from parent 1 to the child2
    parent1_index = 0
    for _ in range(chromosome_length):
        if parent1[parent1_index] not in subset2:
            for j in range(chromosome_length):
                if child2[j] == -1:
                    child2[j] = parent1[parent1_index]
                    parent1_index += 1
                    break
        else:
            parent1_index += 1

    return child1.tolist(), child2.tolist()


def partial_mapped_crossover(
        parent1: List[int],
        parent2: List[int],
        seed: int = 42,
    ) -> Tuple[List[int], List[int]]:
    """
    Implementation of the Partial Mapped Crossover algorithm

    Thanks to
    https://observablehq.com/@swissmanu/pmx-crossover
    for code inspiration

    :param parent1: List[int] - the first parent chromosome
    :param parent2: List[int] - the second parent chromosome
    :param seed: int - random seed
    :return: Tuple[List[int], List[int]] - the two child chromosomes
    """

    np.random.seed(seed)

    # Get the length of the chromosome
    assert len(parent1) == len(parent2), 'The length of the chromosomes should be the same'
    chromosome_length = len(parent1)

    random_subset = np.random.randint(0, chromosome_length, 2)
    start, end = min(random_subset), max(random_subset)

    child1 = parent1[:]
    child2 = parent2[:]
    mapping1 = {}
    mapping2 = {}

    # Map Slice:
    for i in range(start, end):
        mapping1[parent2[i]] = parent1[i]
        child1[i] = parent2[i]

        mapping2[parent1[i]] = parent2[i]
        child2[i] = parent1[i]

    # Repair Lower Slice:
    for i in range(start):
        while child1[i] in mapping1:
            child1[i] = mapping1[child1[i]]
        while child2[i] in mapping2:
            child2[i] = mapping2[child2[i]]

    # Repair Upper Slice:
    for i in range(end, len(child1)):
        while child1[i] in mapping1:
            child1[i] = mapping1[child1[i]]
        while child2[i] in mapping2:
            child2[i] = mapping2[child2[i]]

    return child1, child2
