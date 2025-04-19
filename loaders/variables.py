"""
================================================================================
  Author: Abhishek Prajapati
  File: variables.py

  Description:
    This module provides functionality to load user-defined variables from 
    YAML-formatted files for use in Terraform template rendering.

================================================================================
"""

import os
import yaml

# Directory where all variable files are stored
vars_dir = "./variables"

def load_vars(name: str = "terrapy.vars"):
    """
    Loads variables from a specified YAML file.

    Args:
        name (str): The name of the variable file to load (default is 'terrapy.vars').

    Returns:
        tuple[dict, Exception | None]:
            - A dictionary containing the loaded variables.
            - An Exception object if the file is not found or cannot be loaded; otherwise None.
    """
    vars = dict()
    error = None

    print(f"Loading variables from the following variable file: {name}")

    # Construct the full path to the variable file
    vars_file_path = os.path.join(vars_dir, name)

    # Check if the variable file exists
    if not os.path.exists(vars_file_path):
        error = FileNotFoundError(
            f"Unable to load variables from {name} as it does not exist at: {vars_file_path}"
        )
        return vars, error

    # Load variables from the YAML file using a safe loader
    with open(vars_file_path) as vars_f:
        vars = yaml.load(vars_f, Loader=yaml.SafeLoader)

    return vars, error
