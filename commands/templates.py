from . import *
import os
import pathlib
import tempfile
import io
import PIL.Image
import matplotlib.pyplot as plt
from graphviz import Source  # Assuming you're using graphviz to render Terraform graphs

class Templates:
    def __init__(self, cli):
        """
        Constructor for the Templates class.

        Parameters:
        - cli: A command-line interface object (likely from a CLI framework like Click or Typer).

        Initializes:
        - A Terraform instance.
        - Registers the 'templates' method as a CLI command so it can be used from the terminal.
        """
        self.terraform = Terraform()
        cli.command()(self.templates)

    def templates(self, name: str, vars: str = "terrapy.vars"):
        """
        Renders and displays Terraform template files for a given module/environment.

        Parameters:
        - name (str): The name of the module/environment to render.
        - vars (str): The path to the variable file used in rendering (default: 'terrapy.vars').

        What it does:
        1. Calls `get_rendered_tf_files()` to generate Terraform config files from templates.
        2. Prints each rendered file with formatting.
        3. Validates each rendered file using `terraform validate`.
        4. If validation is successful, generates and displays a visual graph of Terraform resources.
        """

        # Generate/render the Terraform files
        files, err = get_rendered_tf_files(name, vars)

        # Print and handle error if rendering fails
        if err is not None:
            print(err)
        else:
            # Iterate over each rendered file
            for file_name, content in files.items():
                print("*" * 20)
                print(f"{file_name}:")
                print("*" * 20)
                print(content)

                # Create a temporary directory to validate and graph the file
                with tempfile.TemporaryDirectory() as tmp_file:
                    # Construct temporary file path using file name (without extension)
                    tmp = os.path.join(tmp_file, pathlib.Path(file_name).stem)

                    # Write the rendered content to a temporary file
                    with open(tmp, "w") as tmp_f:
                        tmp_f.write(content)

                    # Save the current Terraform working directory
                    old_dir = self.terraform.working_dir

                    # Point Terraform to the temporary directory
                    self.terraform.working_dir = tmp_file

                    # Initialize Terraform in that temporary directory
                    self.terraform.init()

                    # Validate the Terraform configuration
                    exit_code, message, err = self.terraform.cmd("validate")
                    print("Exit Code: ", exit_code)
                    print("Message: ", message)
                    print("Error: ", err)

                    # Generate and render Terraform graph if validation passed
                    exit_code, content, _ = self.terraform.cmd("graph")
                    if exit_code == 0:
                        # Render graph using Graphviz and display as an image
                        graph = Source(content)
                        png_data = graph.pipe(format='png')
                        image = PIL.Image.open(io.BytesIO(png_data))

                        # Display the image using matplotlib
                        plt.imshow(image)
                        plt.axis('off')
                        plt.show()

                    # Restore the original Terraform working directory
                    self.terraform.working_dir = old_dir
