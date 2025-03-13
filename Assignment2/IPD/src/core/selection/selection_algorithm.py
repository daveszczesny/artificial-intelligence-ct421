import numpy as np

def tournament_selection(
        agents: list,
        selects: int = 2,
        tournament_size: int = 2,
) -> list:
    """
    Tournament Selection
    this function selects the best strategies from a random subset
    :param strategies - a list of the strategies
    :param selects: int - the number of strategies to select
    :param tournament_size: int - the size of the tournament
    :return: list
    """

    selected_agents_index = []
    for _ in range(selects):
        tournament_indices = np.random.choice(
            len(agents),
            size=tournament_size,
            replace=False,
        )
        tournament_fitness = [agents[i].fitness for i in tournament_indices]
        best_index = tournament_indices[np.argmax(tournament_fitness)]
        selected_agents_index.append(best_index)

    selected_agents = [agents[i] for i in selected_agents_index]
    return selected_agents