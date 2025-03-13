from enum import Enum
from typing import List, Dict, Callable
import random as rnd

from core.models.action import Action


class Strategy(Enum):
    ALWAYS_COOPERATE = "Always Cooperate"
    ALWAYS_DEFECT = "Always Defect"
    TIT_FOR_TAT = "Tit for Tat"
    RANDOM = "Random"
    GRIM_TRIGGER = "Grim Trigger"
    PAVLOV = "Pavlov"



def always_cooperate(count: int) -> List[Action]:
    return [Action.COOPERATE for _ in range(count)]

def always_defect(count: int) -> List[Action]:
    return [Action.DEFECT for _ in range(count)]

def tit_for_tat(count: int, other_strategy: List[Action]) -> List[Action]:
    """
    Do what the other agent did last round.
    1. The first action is cooperate.
    2. The following actions are the n-1 action of the other agent
    """
    actions = [Action.COOPERATE]
    for action in other_strategy:
        if len(actions) >= count:
            break

        actions.append(action)
    return actions

def random(count: int) -> List[Action]:
    return [rnd.choice([Action.COOPERATE, Action.DEFECT]) for _ in range(count)]


def grim_trigger(count: int, other_strategy: List[Action]) -> List[Action]:
    """
    Cooperate until the other agent defects, then alway defect
    """
    actions = []
    defected = False
    for action in other_strategy:
        if defected:
            actions.append(Action.DEFECT)
        else:
            if action == Action.DEFECT:
                defected = True
            actions.append(Action.COOPERATE)
    return actions

def pavlov(count: int, other_strategy: List[Action]) -> List[Action]:
    """
    cooperate if both agents did the same thing in the previous round, otherwise defect
    """
    actions = [Action.COOPERATE]
    for i in range(1, count):
        if other_strategy[i] == actions[i-1]:
            actions.append(Action.COOPERATE)
        else:
            actions.append(Action.DEFECT)
    return actions


strategy_functions: Dict[Strategy, Callable[..., List[Action]]] = {
    Strategy.ALWAYS_COOPERATE: always_cooperate,
    Strategy.ALWAYS_DEFECT: always_defect,
    Strategy.TIT_FOR_TAT: tit_for_tat,
    Strategy.RANDOM: random,
    Strategy.GRIM_TRIGGER: grim_trigger,
    Strategy.PAVLOV: pavlov,
}

opponent_based_strategies: List[Strategy] = [
    Strategy.GRIM_TRIGGER, Strategy.PAVLOV, Strategy.TIT_FOR_TAT
]

def get_strategy(strategy: Strategy, count: int, other_strategy: List[Action] = None) -> List[Action]:
    """
    function to call selected strategy without manually calling strategy function
    """
    if strategy in opponent_based_strategies:
        if other_strategy is None:
            raise ValueError(f"{strategy.value} strategy requires other strategy as a parameter")
        return strategy_functions[strategy](count, other_strategy)
    else:
        return strategy_functions[strategy](count)
