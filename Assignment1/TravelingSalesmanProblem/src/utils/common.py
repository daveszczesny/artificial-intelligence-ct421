import numpy as np

from typing import List, Tuple, Callable

def euclidean(
        point1: Tuple[float, float],
        point2: Tuple[float, float]
        ) -> float:
    # Euclidean distance between two points
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5


def calculate_distance(
        city1: Tuple[float, float],
        city2: Tuple[float, float],
        heuristic: Callable = euclidean
        ) -> float:
    """
    Calculate the distance between two cities
    :param city1: Tuple[float, float]
    :param city2: Tuple[float, float]
    :param heuristic: function to calculate distance between city 1 and city 2
    :return: float
    """
    return heuristic(city1, city2)

def generate_distance_matrix(
        dimension: int,
        cities: List[Tuple[float, float]]
        ) -> np.ndarray:
    distance_matrix = np.zeros((dimension, dimension))

    for i in range(dimension):
        for j in range(i + 1, dimension):
            # since distance between cities i and j is the same as j and i
            # we can calculate the distance once and assign it to both

            distance = calculate_distance(cities[i], cities[j])
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance

    return distance_matrix

def calculate_total_distance_for_population(population: List[List[int]], distance_matrix: np.ndarray):
    return [calculate_total_distance(individual, distance_matrix) for individual in population]

def calculate_total_distance(
        chromosomes: List[int],
        distance_matrix: np.ndarray
        ) -> np.float64:
    total_distance: float = 0.0
    for i in range(len(chromosomes) - 1):
        total_distance += distance_matrix[chromosomes[i]][chromosomes[i + 1]]

    # Add the distance from the last city back to the first city
    total_distance += distance_matrix[chromosomes[-1]][chromosomes[0]]
    return total_distance