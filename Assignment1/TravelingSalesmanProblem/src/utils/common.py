import json
import numpy as np

def np_to_python(d):
    """
    Convert NumPy data types to regular Python data types
    """
    if isinstance(d, dict):
        return {k: np_to_python(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [np_to_python(v) for v in d]
    elif isinstance(d, np.ndarray):  # Handling NumPy arrays
        return d.tolist()  # Convert numpy array to list
    elif isinstance(d, (np.int64, np.int32)):  # Handle numpy integer types
        return int(d)  # Convert numpy int to regular Python int
    elif isinstance(d, (np.float64, np.float32)):  # Handle numpy float types
        return float(d)  # Convert numpy float to regular Python float
    else:
        return d  # Return the data as-is if it's not a numpy type

def write_to_json(data, file_path):
    """
    Write data to a JSON file
    """
    with open(file_path, 'w') as f:
        f.write(json.dumps(data, indent=4))