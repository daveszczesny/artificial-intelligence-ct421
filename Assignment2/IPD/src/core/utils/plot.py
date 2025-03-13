import matplotlib.pyplot as plt

from core.models.action import Action


def plot_strategy_versus_other(strategy, other):
    strategy_actions = [1 if action == Action.COOPERATE else 0 for action in strategy]
    other_actions = [1 if action == Action.COOPERATE else 0 for action in other]
    indices = list(range(len(strategy)))

    plt.plot(indices, strategy_actions, label='My Strategy', color='blue')
    plt.plot(indices, other_actions, label='Other Strategy', color='red')
    plt.xlabel("Step")
    plt.ylabel("Action (1 = Cooperate, 0 = Defect)")
    plt.title("Strategy vs Other Strategy")
    plt.legend()
    plt.show()

def plot_fitness_over_time(fitness_history):
    plt.plot(fitness_history)
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.title("Fitness Progression")
    plt.show()

def plot_cooperation_versus_defect(agent_strategy, cluster: str = None):
    cooperation_count = sum(1 for action in agent_strategy if action == Action.COOPERATE)
    defect_count = sum(1 for action in agent_strategy if action == Action.DEFECT)

    labels = ['Cooperate', 'Defect']
    counts = [cooperation_count, defect_count]

    plt.bar(labels, counts, color=['blue', 'red'])
    plt.xlabel("Action")
    plt.ylabel("Count")
    if cluster is None:
        plt.title("Cooperation vs Defect in Agent Strategy")
    else:
        plt.title(f"Cluster: {cluster} - Cooperation vs Defect in Agent Strategy")
    plt.show()

def plot_cooperation_and_defect_over_time(strategy_history):
    cooperation_counts = []
    defect_counts = []

    for strategy in strategy_history:
        cooperation_count = sum(1 for action in strategy if action == Action.COOPERATE)
        defect_count = sum(1 for action in strategy if action == Action.DEFECT)
        cooperation_counts.append(cooperation_count)
        defect_counts.append(defect_count)

    plt.plot(cooperation_counts, label='Cooperate', color='blue')
    plt.plot(defect_counts, label='Defect', color='red')
    plt.xlabel("Time")
    plt.ylabel("Count")
    plt.title("Cooperation and Defect Over Time")
    plt.legend()
    plt.show()



def plot_multi_agents_fitness_over_time(fitness_history_of_agents):
    for i, fitness_history in enumerate(fitness_history_of_agents):
        plt.plot(fitness_history, label=f'Cluster {i+1}')
    
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title('Fitness of Best Agent in Each Cluster Over Time')
    plt.legend()
    plt.show()

def plot_multi_agents_cooperation_and_defect_over_time(cooperation_count, defection_count):
    plt.plot(cooperation_count, label='Cooperate', color='blue')
    plt.plot(defection_count, label='Defect', color='red')

    plt.xlabel("Generation")
    plt.ylabel("Count")
    plt.title('Cooperation and Defection Over Time')
    plt.legend()
    plt.show()
