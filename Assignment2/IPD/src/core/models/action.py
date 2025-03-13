from enum import Enum


class Action(Enum):
    COOPERATE = 1
    DEFECT = 0

    def __str__(self):
        return self.name
