"""
================================================================================
  Author: Abhishek Prajapati
  File: main.py

  Contact: prajapatiabhishek1996@gmail.com

  Description:
    This script defines the CLI entry point using the Typer framework. It 
    initializes and registers CLI command modules for templates and apply logic.

  License & Usage:
    This code is provided for use as-is and may be used freely for educational or
    operational purposes. However, duplication, recreation, modification, or 
    redistribution of this code (in part or whole) is strictly prohibited without 
    prior written permission from the author.

    © Abhishek Prajapati. All rights reserved.
================================================================================
"""

from typer import Typer
from commands.templates import Templates
from commands.apply import Apply

cli = Typer()

Templates(cli)
Apply(cli)

if __name__ == "__main__":
    cli()
