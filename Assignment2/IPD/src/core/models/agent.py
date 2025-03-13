from typing import List

from core.models.action import Action

class Agent:
    def __init__(self, strategy: List[Action], fitness: float = 0):
        self.strategy = strategy
        self.fitness = fitness

    def next_action(self):
        if len(self.strategy) == 0:
            raise ValueError("Strategy is empty")
        return self.strategy.pop(0)

    def print_strategy(self):
        clean_strat = [action.value for action in self.strategy]
        for i, action in enumerate(clean_strat):
            if action == 1:
                clean_strat[i] = 'C'
            else:
                clean_strat[i] = 'D'
        return clean_strat
