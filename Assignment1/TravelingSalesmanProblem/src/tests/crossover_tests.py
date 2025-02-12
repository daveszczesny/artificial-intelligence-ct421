import numpy as np
from core import genetic_algorithm


time_taken_pmx = []
distance_pmx = []

for i in range(20):
    print(f'Running PMX crossover {i + 1}')
    info = genetic_algorithm.run(
        generations=1_000,
        chance_of_mutation=15,
        crossover_type={'PMX': 100},
        )
    time_taken_pmx.append(info['time_taken'])
    distance_pmx.append(info['best_individual']['distance'])


time_taken_ox = []
distance_ox = []

for i in range(20):
    print(f'Running OX crossover {i + 1}')
    info = genetic_algorithm.run(
        generations=1_000,
        chance_of_mutation=15,
        crossover_type={'OX': 100},
        )
    time_taken_ox.append(info['time_taken'])
    distance_ox.append(info['best_individual']['distance'])

# get the min, max, mean, and std of the time taken for the PMX and OX crossover
time_taken_pmx = np.array(time_taken_pmx)
time_taken_ox = np.array(time_taken_ox)

distance_pmx = np.array(distance_pmx)
distance_ox = np.array(distance_ox)

pmx_min = np.min(time_taken_pmx)
pmx_max = np.max(time_taken_pmx)
pmx_mean = np.mean(time_taken_pmx)
pmx_std = np.std(time_taken_pmx)
distance_pmx_std = np.std(distance_pmx)
distance_pmx_mean = np.mean(distance_pmx)

ox_min = np.min(time_taken_ox)
ox_max = np.max(time_taken_ox)
ox_mean = np.mean(time_taken_ox)
ox_std = np.std(time_taken_ox)
distance_ox_std = np.std(distance_ox)
distance_ox_mean = np.mean(distance_ox)

print('PMX Crossover:')
print(f'Min: {pmx_min}')
print(f'Max: {pmx_max}')
print(f'Mean: {pmx_mean}')
print(f'Std: {pmx_std}')
print(f'std distance {distance_pmx_std}')
print(f'Mean distance {distance_pmx_mean}')

print('OX Crossover:')
print(f'Min: {ox_min}')
print(f'Max: {ox_max}')
print(f'Mean: {ox_mean}')
print(f'Std: {ox_std}')
print(f'std distance {distance_ox_std}')
print(f'Mean distance {distance_ox_mean}')



time_taken = {'80:20': [], '90:10': [], '70:30': [], '50:50': []}
distance = {'80:20': [], '90:10': [], '70:30': [], '50:50': []}

for i in range(10):
    info = genetic_algorithm.run(
        generations=1_000,
        chance_of_mutation=15,
        crossover_type={'PMX': 80, 'OX': 20},
        )
    time_taken['80:20'].append(info['time_taken'])
    distance['80:20'].append(info['best_individual']['distance'])

for i in range(10):
    info = genetic_algorithm.run(
        generations=1_000,
        chance_of_mutation=15,
        crossover_type={'PMX': 90, 'OX': 10},
        )
    time_taken['90:10'].append(info['time_taken'])
    distance['90:10'].append(info['best_individual']['distance'])

for i in range(10):
    info = genetic_algorithm.run(
        generations=1_000,
        chance_of_mutation=15,
        crossover_type={'PMX': 70, 'OX': 30},
        )
    time_taken['70:30'].append(info['time_taken'])
    distance['70:30'].append(info['best_individual']['distance'])

for i in range(10):
    info = genetic_algorithm.run(
        generations=1_000,
        chance_of_mutation=15,
        crossover_type={'PMX': 50, 'OX': 50},
        )
    time_taken['50:50'].append(info['time_taken'])
    distance['50:50'].append(info['best_individual']['distance'])


# get the min, max, mean, and std of the time taken for the PMX and OX crossover
time_taken_8020 = np.array(time_taken['80:20'])
time_taken_9010 = np.array(time_taken['90:10'])
time_taken_7030 = np.array(time_taken['70:30'])
time_taken_5050 = np.array(time_taken['50:50'])

distance_8020 = np.array(distance['80:20'])
distance_9010 = np.array(distance['90:10'])
distance_7030 = np.array(distance['70:30'])
distance_5050 = np.array(distance['50:50'])

time_taken_8020_min = np.min(time_taken_8020)
time_taken_8020_max = np.max(time_taken_8020)
time_taken_8020_mean = np.mean(time_taken_8020)
time_taken_8020_std = np.std(time_taken_8020)
distance_8020_std = np.std(distance_8020)
distance_8020_mean = np.mean(distance_8020)

time_taken_9010_min = np.min(time_taken_9010)
time_taken_9010_max = np.max(time_taken_9010)
time_taken_9010_mean = np.mean(time_taken_9010)
time_taken_9010_std = np.std(time_taken_9010)
distance_9010_std = np.std(distance_9010)
distance_9010_mean = np.mean(distance_9010)

time_taken_7030_min = np.min(time_taken_7030)
time_taken_7030_max = np.max(time_taken_7030)
time_taken_7030_mean = np.mean(time_taken_7030)
time_taken_7030_std = np.std(time_taken_7030)
distance_7030_std = np.std(distance_7030)
distance_7030_mean = np.mean(distance_7030)

time_taken_5050_min = np.min(time_taken_5050)
time_taken_5050_max = np.max(time_taken_5050)
time_taken_5050_mean = np.mean(time_taken_5050)
time_taken_5050_std = np.std(time_taken_5050)
distance_5050_std = np.std(distance_5050)
distance_5050_mean = np.mean(distance_5050)

print('80:20 Crossover:')
print(f'Min: {time_taken_8020_min}')
print(f'Max: {time_taken_8020_max}')
print(f'Mean: {time_taken_8020_mean}')
print(f'Std: {time_taken_8020_std}')
print(f'std distance {distance_8020_std}')
print(f'Mean distance {distance_8020_mean}')

print('90:10 Crossover:')
print(f'Min: {time_taken_9010_min}')
print(f'Max: {time_taken_9010_max}')
print(f'Mean: {time_taken_9010_mean}')
print(f'Std: {time_taken_9010_std}')
print(f'std distance {distance_9010_std}')
print(f'Mean distance {distance_9010_mean}')

print('70:30 Crossover:')
print(f'Min: {time_taken_7030_min}')
print(f'Max: {time_taken_7030_max}')
print(f'Mean: {time_taken_7030_mean}')
print(f'Std: {time_taken_7030_std}')
print(f'std distance {distance_7030_std}')
print(f'Mean distance {distance_7030_mean}')

print('50:50 Crossover:')
print(f'Min: {time_taken_5050_min}')
print(f'Max: {time_taken_5050_max}')
print(f'Mean: {time_taken_5050_mean}')
print(f'Std: {time_taken_5050_std}')
print(f'std distance {distance_5050_std}')
print(f'Mean distance {distance_5050_mean}')
