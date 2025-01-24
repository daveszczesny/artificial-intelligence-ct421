import copy
from typing import List

import numpy as np

def swap_mutation(_individual: List[int], seed: int = 42):
    """
    Swap mutation
    This function randomly selects two genes in the individual and swaps their positions
    :param individual: List[int] - the individual to mutate
    :return: List[int] - the mutated individual
    """
    individual = copy.deepcopy(_individual)

    np.random.seed(seed)

    chromosome_length = len(individual)
    mutation_points = np.random.randint(0, chromosome_length, 2)

    individual[mutation_points[0]], individual[mutation_points[1]] = individual[mutation_points[1]], individual[mutation_points[0]]
    return individual


def scramble_mutation(_individual: List[int], seed: int = 42):
    """
    Scramble mutation
    This function randomly selects a subset of genes in the individual and shuffles their positions
    :param individual: List[int] - the individual to mutate
    :return: List[int] - the mutated individual
    """

    individual = copy.deepcopy(_individual)
    np.random.seed(seed)

    chromosome_length = len(individual)
    random_subet = np.random.randint(0, chromosome_length, 2)
    start, end = min(random_subet), max(random_subet)

    subset = individual[start:end]
    np.random.shuffle(subset)
    individual[start:end] = subset

    return individual


def inversion_mutation(_individual: List[int], seed: int = 42):
    """
    Inversion mutation
    This function randomly selects a subset of genes in the individual and reverses their order
    :param individual: List[int] - the individual to mutate
    :return: List[int] - the mutated individual
    """

    individual = copy.deepcopy(_individual)
    np.random.seed(seed)

    chromosome_length = len(individual)
    random_subet = np.random.randint(0, chromosome_length, 2)
    start, end = min(random_subet), max(random_subet)

    subset = individual[start:end]
    subset = subset[::-1]
    individual[start:end] = subset

    return individual
