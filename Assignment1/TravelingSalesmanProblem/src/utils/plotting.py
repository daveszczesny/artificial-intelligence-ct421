from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

def plot_path(path: List[int], cities: List[Tuple[float, float]]):
    x_coords = [cities[i][0] for i in path]
    y_coords = [cities[i][1] for i in path]

    x_coords.append(cities[path[0]][0])
    y_coords.append(cities[path[0]][1])

    plt.scatter(x_coords, y_coords, c='blue', marker='o')

    plt.plot(x_coords, y_coords, c='red')

    plt.title('Best path')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.grid(True)
    plt.show()


def plot_fitness_over_time(tracker: List[Dict[str, int]]):
    x = [t['generation'] for t in tracker]
    y = [t['best_fitness'] for t in tracker]

    plt.plot(x, y)
    plt.title('Fitness over time')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.grid(True)
    plt.show()

def plot_distance_over_time(tracker: List[Dict[str, int]]):
    x = [t['generation'] for t in tracker]
    y = [t['best_distance'] for t in tracker]

    plt.plot(x, y)
    plt.title('Distance over time')
    plt.xlabel('Generation')
    plt.ylabel('Distance')
    plt.grid(True)
    plt.show()
