import os
import logging
from typing import List, Dict, Any, Tuple

import numpy as np

logging.basicConfig(level=logging.INFO, format='%(name)s - %(message)s')
logger = logging.getLogger("TSP Parser")


def load_tsp_file(file_path: str) -> Dict[str, Any]:
    """
    Load a TSP file
    :param file_path: str
    :return: Dict[str, Any], containing the problem name, dimensions and cities
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        raise ValueError("No data in file")

    """
    Steps to read tsp file format
    1. Read the first line to get the problem name
    2. Can ignore line 2 and 3
    3. Dimensions on line 4 can be used to determine the number of cities
    4. Line 5 can be skipped (for now I think)
    5. Ensure this is "NODE_COORD_SECTION"
    6. Read the coordinates of each city until "EOF" is reached
    """

    problem_name = lines[0].strip().split(":")[1].strip()
    logger.info('Detected problem name: %s', problem_name)

    dimensions = int(lines[3].strip().split(':')[1])
    logger.info('Detected dimensions: %d', dimensions)

    cities: List[Tuple[np.float64, np.float64]] = []

    for line in lines[6: ]:
        if 'EOF' in line:
            break

        # Read the coordinates of each city
        # Each line has index, x, y, We can ignore the index
        _, x, y = line.strip().split(' ')
        cities.append((np.float64(x), np.float64(y)))

    assert len(cities) == dimensions, "Number of cities does not match dimensions"

    return {
        'name': problem_name,
        'dimensions': dimensions,
        'cities': cities
    }
