
import numpy as np

def scramble_mutation(
        strategy: list,
):
    genome_length = len(strategy)
    random_subset = np.random.randint(0, genome_length, 2)
    start, end = min(random_subset), max(random_subset)

    subset = strategy[start:end]
    np.random.shuffle(subset)
    strategy[start:end] = subset

    return strategy

def swap_mutation(
        strategy: list,
):
    genome_length = len(strategy)
    mutation_points = np.random.choice(genome_length, 2, replace=False)

    strategy[mutation_points[0]], strategy[mutation_points[1]] = \
        strategy[mutation_points[1]], strategy[mutation_points[0]]
    return strategy