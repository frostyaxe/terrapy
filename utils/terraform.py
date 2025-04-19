"""
================================================================================
  Author: Abhishek Prajapati
  File: renderer.py

  Description:
    This module provides functionality to locate and render all Jinja2-based 
    Terraform templates for a given project. It integrates with variable loaders 
    and template utilities to produce ready-to-use Terraform configuration files.

================================================================================
"""

from .templates import get_all_jinja_templates, render_template
from loaders.variables import load_vars

def get_rendered_tf_files(name: str, vars: str = "terrapy.vars"):
    """
    Loads variable definitions and renders all Jinja2 Terraform templates 
    for the specified project.

    Args:
        name (str): The name of the project directory under the templates folder.
        vars (str, optional): The variable file to load (default is 'terrapy.vars').

    Returns:
        tuple[dict[str, str], Exception | None]:
            - A dictionary where keys are relative file paths and values are rendered template contents.
            - An error object if something fails, otherwise None.
    """
    # Load the variables from the provided file (default: terrapy.vars)
    vars, error = load_vars()
    files = {}

    if error is not None:
        return files, error

    print(f"Looking for Terraform files in the templates folder...")

    # Get all Jinja2 template paths for the specified project
    templates, err = get_all_jinja_templates(name)

    if err is not None:
        return files, err

    # Render each template and store it in the files dictionary
    for template in templates:
        relative_path = template.relative_to("templates").as_posix()
        rendered = render_template(relative_path, vars)
        files[relative_path] = rendered

    return files, None
