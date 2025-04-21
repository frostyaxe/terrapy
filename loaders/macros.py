import pathlib
import os
from jinja2 import Environment, FileSystemLoader

# Initialize the Jinja2 environment with the directory that contains macro templates
env = Environment(loader=FileSystemLoader('macros'))

# Dictionary to store loaded macros by name
macros = {}

# Define the path to the 'macros' directory (assumes it's one level above the current file's parent)
macros_dir = pathlib.Path(
    os.path.join(pathlib.Path(__file__).resolve().parent.parent, "macros")
)

# Find all .j2 macro template files in the 'macros' directory
macro_files = macros_dir.glob("*.j2")

def load_macros():
    """
    Load all macros from Jinja2 templates located in the 'macros' directory.

    Returns:
        dict: A dictionary where the key is the macro file name (without extension)
              and the value is the loaded template module containing macros.
    """
    for macro_file in macro_files:
        # Load the template using its file name
        tpl = env.get_template(macro_file.name)

        # Store the macro module using the file name (without .j2 extension) as the key
        macros[macro_file.stem] = tpl.module

    return macros
