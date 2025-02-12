from typing import List, Tuple
import numpy as np

from core.models.population import Population, Individual

"""
source: https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_parent_selection.htm
"""

def roulette_wheel_selection(
        population: Population,
        selects: int = 2,
    ) -> List[int]:
    """
    Roulette wheel selection
    This function creates a roulette wheel based on the fitness of the population
    Individuals with higher fitness have a higher chance of being selected
    :param population_fitness: List[np.float64] - the fitness of each individual in the population
    :return: Tuple[int, int] - the indices of the selected individuals
    """

    population_fitness = [individual.fitness for individual in population.individuals]
    total_fitness = np.sum(population_fitness)
    selection_probabilities = [fitness / total_fitness for fitness in population_fitness]
    selected_indices = np.random.choice(len(population_fitness), size=selects, p=selection_probabilities)

    selected_individuals = [population.individuals[i] for i in selected_indices]
    return selected_individuals

def tournament_selection(
        population: Population,
        selects: int = 2,
        tournament_size: int = 2,
    ) -> List[Individual]:
    """
    Tournament selection
    This function selects the best individual from a random subset of the population
    :param population_fitness: List[np.float64] - the fitness of each individual in the population
    :param selects: int - the number of individuals to select
    :param tournament_size: int - the size of the tournament
    :param seed: int - random seed
    :return: List[int] - the list of the selected individuals
    """

    selected_individuals_index: List[np.int64] = []

    for _ in range(selects):
        tournament_indices = np.random.choice(len(population.individuals), size=tournament_size, replace=False)
        tournament_fitness = [population.individuals[i].fitness for i in tournament_indices]
        best_index = tournament_indices[np.argmax(tournament_fitness)]
        selected_individuals_index.append(best_index)

    selected_individuals = [population.individuals[i] for i in selected_individuals_index]
    return selected_individuals
