import numpy as np

from core.models.population import Individual


def swap_mutation(
        individual: Individual,
    ) -> Individual:
    """
    Swap mutation
    This function randomly selects two genes in the individual and swaps their positions
    O(1) time complexity
    :param individual: List[int] - the individual to mutate
    :return: List[int] - the mutated individual
    """
    chromosome_length = len(individual.path)
    mutation_points = np.random.choice(chromosome_length, 2, replace=False)

    individual.path[mutation_points[0]], individual.path[mutation_points[1]] = \
        individual.path[mutation_points[1]], individual.path[mutation_points[0]]
    return individual


def scramble_mutation(
        individual: Individual,
    ):
    """
    Scramble mutation
    This function randomly selects a subset of genes in the individual and shuffles their positions
    O(n) time complexity
    :param individual: List[int] - the individual to mutate
    :return: List[int] - the mutated individual
    """

    chromosome_length = len(individual.path)
    random_subet = np.random.randint(0, chromosome_length, 2)
    start, end = min(random_subet), max(random_subet)

    subset = individual.path[start:end]
    np.random.shuffle(subset)
    individual.path[start:end] = subset

    return individual


def inversion_mutation(
        individual: Individual,
    ):
    """
    Inversion mutation
    This function randomly selects a subset of genes in the individual and reverses their order
    O(n) time complexity
    :param individual: List[int] - the individual to mutate
    :return: List[int] - the mutated individual
    """

    chromosome_length = len(individual.path)
    random_subet = np.random.randint(0, chromosome_length, 2)
    start, end = min(random_subet), max(random_subet)

    subset = individual.path[start:end]
    subset = subset[::-1]
    individual.path[start:end] = subset

    return individual
