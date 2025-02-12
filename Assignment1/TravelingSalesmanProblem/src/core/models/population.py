
from typing import List, Dict, Any
from dataclasses import dataclass

import numpy as np

class Individual:

    def __init__(
            self, path: List[int],
            distance: np.float64,
            fitness: np.float64
        ):
        self.path = path
        self.distance = distance
        self.fitness = fitness

    def __eq__(self, other):
        if isinstance(other, Individual):
            return self.path == other.path
        return False

    def __hash__(self):
        return hash(tuple(self.path))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'path': self.path,
            'distance': self.distance,
            'fitness': self.fitness
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Individual':
        return cls(
            path=data['path'],
            distance=data['distance'],
            fitness=data['fitness']
        )

@dataclass
class Population:
    individuals: List[Individual] # defines the individuals in the population