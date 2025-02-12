from typing import List, Callable
import numpy as np

from core.evaluation.heuristic_functions import _inverse_distance_heuristic

def calculate_fitness(
        total_distance: np.float64,
        heuristic: Callable =_inverse_distance_heuristic,
        ) -> np.float64:
    return np.float64(heuristic(total_distance))

def calculate_fitness_of_population(
        total_distances: List[np.float64],
        heuristic: Callable = _inverse_distance_heuristic
        ) -> List[np.float64]:
    return [calculate_fitness(total_distance, heuristic) for total_distance in total_distances]
