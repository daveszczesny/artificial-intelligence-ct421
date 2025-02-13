import random
from enum import Enum
from typing import List, Dict
from core.models.population import Individual
from core.crossover.crossover_alogrithm import ordered_crossover, partial_mapped_crossover

class CrossoverType(Enum):
    OX = 'ox'
    PMX = 'pmx'

def apply_crossover(
        parents: List[Individual],
        crossover_type: Dict[CrossoverType, int],
        chance_of_crossover: int,
    ):
    offspring: List[Individual] = []
    random.shuffle(parents)

    for i in range(0, len(parents), 2):
        if i + 1 >= len(parents):
            # if we have an odd number of parents, we just add the last parent to the offspring
            offspring.append(parents[i])
            break

        # Perform Crossover
        if random.randint(0, 100) < chance_of_crossover:
            if CrossoverType.OX in crossover_type and \
                CrossoverType.PMX in crossover_type:
                crossover_type_chance = random.randint(0, 100)
                if crossover_type_chance < crossover_type[CrossoverType.OK]:
                    child1, child2 = ordered_crossover(parents[i], parents[i+1])
                else:
                    child1, child2 = partial_mapped_crossover(parents[i], parents[i+1])
            elif CrossoverType.OX in crossover_type:
                child1, child2 = ordered_crossover(parents[i], parents[i+1])
            else: # PMX
                child1, child2 = partial_mapped_crossover(parents[i], parents[i+1])

            offspring.append(child1)
            offspring.append(child2)
        else:
            # if no crossover is performed, we just add the parents to the offspring
            offspring.append(parents[i])
            offspring.append(parents[i+1])

    return offspring
