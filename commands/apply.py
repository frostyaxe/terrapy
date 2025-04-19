from . import *
import os
import pathlib

class Apply:
    def __init__(self, cli):
        """
        Constructor for the Apply class.

        Parameters:
        - cli: A command-line interface object (likely from a CLI framework such as Click or Typer),
               which is used to register command-line commands.

        Initializes:
        - A Terraform instance used to execute Terraform commands like init, plan, and apply.
        - Registers the apply method as a command-line command using the provided CLI object.
        """
        self.terraform = Terraform()  # Create a Terraform object instance
        cli.command()(self.apply)     # Register the 'apply' method as a CLI command

    def apply(self, name: str):
        """
        Apply Terraform configuration for the given environment/module name.

        Parameters:
        - name (str): Name of the module/environment to which Terraform should be applied.
                      This name determines the configuration files and the working directory.

        Steps:
        1. Generate/render Terraform configuration files.
        2. Write the rendered files into a structured directory.
        3. Set up the working directory for Terraform execution.
        4. Run `terraform init`, `terraform plan`, and `terraform apply`.
        5. Print out logs and restore the original working directory.
        """

        # Render the Terraform files for the given module/environment name using provided variables
        files, err = get_rendered_tf_files(name, vars)

        # If an error occurred while rendering the files, print it and exit early
        if err is not None:
            print(err)

        # Write each rendered file to the appropriate directory under ./terraform/
        for file_path, content in files.items():
            # Create the complete file path
            file_path = pathlib.Path(os.path.join("./terraform", file_path))

            # Ensure the parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Remove any file extension (like .tmpl, .j2, etc.) and convert to POSIX format
            file_path = file_path.with_suffix("").as_posix()

            # Write the rendered content to the file
            with open(file_path, "w") as file:
                file.write(content)

        # Backup the current working directory to restore later
        old_dir = self.terraform.working_dir

        # Set the Terraform working directory for the current module
        self.terraform.working_dir = os.path.join("./terraform", name)

        # Initialize the Terraform configuration (downloads providers, sets backend, etc.)
        self.terraform.init()

        # Run `terraform plan` to preview changes
        exit_code, message, error = self.terraform.plan()
        print("Exit Code: ", exit_code)
        print("Message: ", message)
        print("Error: ", error)

        # Run `terraform apply` to apply the changes, auto-approving without user input
        exit_code, message, error = self.terraform.apply(auto_approve=True)
        print("Exit Code: ", exit_code)
        print("Message: ", message)
        print("Error: ", error)

        # Restore the original Terraform working directory
        self.terraform.working_dir = old_dir
