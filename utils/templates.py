"""
================================================================================
  Author: Abhishek Prajapati
  File: template_renderer.py

  Description:
    This module handles the loading and rendering of Jinja2 templates used in 
    Terraform or configuration generation workflows. It searches for `.j2` template 
    files under a project-specific directory and renders them with provided variables.

================================================================================
"""

from jinja2 import FileSystemLoader, Environment
import os
import pathlib

# Define the root directory where all Jinja2 templates are stored
templates = "./templates"

# Set up the Jinja2 environment with a file system loader pointing to the templates directory
tpl_env = Environment(loader=FileSystemLoader(templates))

def get_all_jinja_templates(project_name):
    """
    Retrieves all `.j2` (Jinja2) template files recursively under a given project directory.

    Args:
        project_name (str): The name of the project folder inside the templates directory.

    Returns:
        (list[pathlib.Path], Exception | None): 
            - A list of Path objects representing all `.j2` files found.
            - None if no error, otherwise an Exception if the path does not exist.
    """
    tpl_project_path = os.path.join(templates, project_name)
    if not os.path.exists(tpl_project_path):
        return [], Exception(f"Template project does not exist at the given path: {tpl_project_path}")
    
    project_path_obj = pathlib.Path(tpl_project_path)
    return [file for file in project_path_obj.rglob("*j2")], None

def render_template(path: str, vars):
    """
    Renders a Jinja2 template using the provided variables.

    Args:
        path (str): Relative path to the template file from the templates root.
        vars (dict): Dictionary of variables to be used for rendering the template.

    Returns:
        str: Rendered template content as a string.
    """
    tpl = tpl_env.get_template(path)
    return tpl.render(vars)
