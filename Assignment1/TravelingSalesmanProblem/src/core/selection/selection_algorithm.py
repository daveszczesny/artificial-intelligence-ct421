from typing import List, Tuple
import numpy as np

"""
source: https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_parent_selection.htm
"""

def roulette_wheel_selection(
        population_fitness: List[np.float64],
        selects: int = 2,
        seed: int = 42
    ) -> List[int]:
    """
    Roulette wheel selection
    This function creates a roulette wheel based on the fitness of the population
    Individuals with higher fitness have a higher chance of being selected
    :param population_fitness: List[np.float64] - the fitness of each individual in the population
    :return: Tuple[int, int] - the indices of the selected individuals
    """

    total_fitness = np.sum(population_fitness)
    selection_probabilities = [fitness / total_fitness for fitness in population_fitness]

    np.random.seed(seed)
    selected_individuals = np.random.choice(len(population_fitness), size=selects, p=selection_probabilities)

    return selected_individuals

def tournament_selection(
        population_fitness: List[np.float64],
        selects: int = 2,
        tournament_size: int = 2,
        seed: int = 42
    ) -> List[int]:
    """
    Tournament selection
    This function selects the best individual from a random subset of the population
    :param population_fitness: List[np.float64] - the fitness of each individual in the population
    :param selects: int - the number of individuals to select
    :param tournament_size: int - the size of the tournament
    :param seed: int - random seed
    :return: List[int] - the indices of the selected individuals
    """

    np.random.seed(seed)
    selected_individuals = []
    for _ in range(selects):
        tournament_indices = np.random.choice(len(population_fitness), size=tournament_size, replace=False)
        tournament_fitness = [population_fitness[i] for i in tournament_indices]
        best_index = tournament_indices[np.argmax(tournament_fitness)]
        selected_individuals.append(best_index)

    return selected_individuals
