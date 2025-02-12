import numpy as np
from core import genetic_algorithm

distance_roulette = []
distance_tournament = []

for i in range(10):
    print(f'Running Roulette Wheel Selection {i + 1}')
    info = genetic_algorithm.run(
        generations=1_000,
        chance_of_mutation=15,
        chance_of_crossover=95,
        selection_type='roulette',
        crossover_type={'PMX': 100}
        )
    distance_roulette.append(info['best_individual']['distance'])

for i in range(10):
    print(f'Running Tournament Selection {i + 1}')
    info = genetic_algorithm.run(
        generations=1_000,
        chance_of_mutation=15,
        chance_of_crossover=95,
        selection_type='tournament',
        crossover_type={'PMX': 100}
        )
    distance_tournament.append(info['best_individual']['distance'])

distance_roulette = np.array(distance_roulette)
distance_tournament = np.array(distance_tournament)

roulette_min = np.min(distance_roulette)
roulette_max = np.max(distance_roulette)
roulette_mean = np.mean(distance_roulette)
roulette_std = np.std(distance_roulette)

tournament_min = np.min(distance_tournament)
tournament_max = np.max(distance_tournament)
tournament_mean = np.mean(distance_tournament)
tournament_std = np.std(distance_tournament)

print('Roulette Wheel Selection:')
print(f'Min: {roulette_min}')
print(f'Max: {roulette_max}')
print(f'Mean: {roulette_mean}')
print(f'Std: {roulette_std}')

print('Tournament Selection:')
print(f'Min: {tournament_min}')
print(f'Max: {tournament_max}')
print(f'Mean: {tournament_mean}')
print(f'Std: {tournament_std}')
