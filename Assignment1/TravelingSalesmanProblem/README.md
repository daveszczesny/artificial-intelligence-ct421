# Genetic Algorithm for the Traveling Salesman Problem

@Author: Dawid Szczesny  
@ID: 21300293

## Overview

This project implements a Genetic Algorithm to solve the Traveling Salesman Problem (TSP). The TSP files are located under the `./tsp/` directory.

## Setup

To get started, initialize the virtual environment and install all the dependencies needed for the Python program to run:

```bash
make setup-venv
```

## Running the Program

To run the program, use the following command:

```bash
make run
```

## Customizing the Run

Navigate to `./src/main.py` to customize and optimize your run. The genetic algorithm takes in many different arguments:

1. **Population Size**: Determines the size of the population. Default = 100
2. **Generations**: The number of generations to run. Default = 1,000
3. **Chance of Crossover**: The percentage chance that a crossover will occur per generation. Default = 95
4. **Chance of Mutation**: The percentage chance that a mutation will occur per generated offspring. Default = 15
5. **Elites Size**: The number of elite individuals to keep per generation. Default = 5
6. **File Path**: The file path to the TSP file. Default = `tsp/berlin52.tsp`
7. **Verbose**: If set to 1, will produce extra debug logs. Default = 0
8. **Early Stop**: If the progress halts in the run, it will stop after this number of generations. Default = 1,000
9. **Crossover Type**: The type(s) of crossover to occur in the run. Default = `OX: 50, PMX: 50`
10. **Selection Type**: The type of selection technique to use. Default = `tournament`
11. **Mutation Type**: The type(s) of mutation that could occur in the run. Default = `swap: 50, scramble: 25, inversion: 25`
12. **Write Results**: A boolean value. If set to true, it will write a file output with all the details of the run. Default = `False`
13. **Plot Graphs**: A boolean value. If set to true, it will plot the paths, distance, and fitness graphs at the end of the run. Default = `False`

## Example Usage

Here is an example of how to run the genetic algorithm with custom parameters:

```python
from core import genetic_algorithm
from core.crossover.crossover_algorithm import CrossoverType
from core.mutation.mutation_algorithm import MutationType

genetic_algorithm.run(
    population_size=100,
    generations=1_000,
    chance_of_crossover=95,
    chance_of_mutation=15,
    elites_size=5,
    file_path='tsp/kroA100.tsp',
    verbose=0,
    early_stop=500,
    crossover_type={CrossoverType.OX: 70, CrossoverType.PMX: 30},
    selection_type='roulette',
    mutation_type={MutationType.SWAP: 40, MutationType.SCRAMBLE: 30, MutationType.INVERSION: 30},
    write_results=True,
    plot_graphs=True
)
```

## Results

The results of the run will be saved in a JSON file if `write_results` is set to `True`. The file will contain details of the run, including the best individual, time taken, and highlights of the run.

## Plotting

If `plot_graphs` is set to `True`, the program will generate plots for the paths, distance, and fitness over time.