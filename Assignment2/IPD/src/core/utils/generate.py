import random
from typing import List

from core.models.action import Action
from core.strategy.strategy import Strategy, get_strategy
from core.models.agent import Agent

def generate_random_strategy(count: int) -> List[Action]:
    return [random.choice([Action.COOPERATE, Action.DEFECT]) for _ in range(count)]


def generate_from_strategy(
        count: int,
        strategy: Strategy,
        other_agent_strategy: List[Action] = None
) -> List[Action]:
    return get_strategy(strategy, count, other_agent_strategy)

def generate_agents(agents: int = 100, strategy_count: int = 100) -> List[Agent]:
    """
    generates a list of agents with random strategies
    """
    if strategy_count <= 2:
        raise ValueError('strategy count must be greater than or equal to 2')
    agent_strategies = []
    for _ in range(agents):
        strategy = generate_random_strategy(strategy_count)
        agent = Agent(strategy)
        agent_strategies.append(agent)
    return agent_strategies