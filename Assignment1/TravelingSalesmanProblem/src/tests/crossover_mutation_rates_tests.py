import numpy as np

from core import genetic_algorithm

crossover_rates = [70, 80, 90, 95, 100]
mutation_rates = [5, 10, 15, 20, 25]


crossover_results = {
    '70': [],
    '80': [],
    '90': [],
    '95': [],
    '100': [],
}
for i in range(5):
    for crossover_rate in crossover_rates:
        info = genetic_algorithm.run(
            generations=1000,
            population_size=100,
            early_stop=1000,
            chance_of_crossover=crossover_rate,
            chance_of_mutation=15,
            crossover_type={'PMX': 100},
        )
        crossover_results[str(crossover_rate)].append(info['best_individual']['distance'])

mutation_results = {
    '5': [],
    '10': [],
    '15': [],
    '20': [],
    '25': [],
}

for i in range(5):
    for mutation_rate in mutation_rates:
        info = genetic_algorithm.run(
            generations=1000,
            population_size=100,
            early_stop=1000,
            chance_of_crossover=95,
            chance_of_mutation=mutation_rate,
            crossover_type={'PMX': 100},
        )
        mutation_results[str(mutation_rate)].append(info['best_individual']['distance'])

for crossover_rate in crossover_rates:
    print(f'Crossover Rate: {crossover_rate}')
    print(f'Min: {np.min(crossover_results[str(crossover_rate)])}')
    print(f'Max: {np.max(crossover_results[str(crossover_rate)])}')
    print(f'Mean: {np.mean(crossover_results[str(crossover_rate)])}')
    print(f'Std: {np.std(crossover_results[str(crossover_rate)])}')

for mutation_rate in mutation_rates:
    print(f'Mutation Rate: {mutation_rate}')
    print(f'Min: {np.min(mutation_results[str(mutation_rate)])}')
    print(f'Max: {np.max(mutation_results[str(mutation_rate)])}')
    print(f'Mean: {np.mean(mutation_results[str(mutation_rate)])}')
    print(f'Std: {np.std(mutation_results[str(mutation_rate)])}')
