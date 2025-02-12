from core import genetic_algorithm
from core.crossover.crossover_alogrithm import CrossoverType
from core.mutation.mutation import MutationType

genetic_algorithm.run(
    generations=25_000,
    early_stop=1_500,
    population_size=100,
    chance_of_crossover=95,
    chance_of_mutation=15,
    crossover_type={
        CrossoverType.PMX: 10,
        CrossoverType.OX: 90
    },
    mutation_type={
        MutationType.INVERSION: 25,
        MutationType.SCRAMBLE: 25,
        MutationType.SWAP: 50,
    },
    file_path='tsp/kroA100.tsp',
    write_results=True,
    plot_graphs=True
)
