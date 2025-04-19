# 🌍 terrapy

**terrapy** is a lightweight CLI tool that automates the generation, validation, and application of Terraform templates using Python. It integrates seamlessly with the Terraform CLI and provides a programmable interface to work with infrastructure-as-code.

## ✨ Features

- 🔧 Render Terraform configuration files from templates
- ✅ Automatically validate rendered configurations
- 📈 Visualize Terraform resource graphs
- 🚀 Apply infrastructure changes via Terraform CLI
- 🧩 CLI integration using frameworks like Click or Typer

## 📦 Requirements

Make sure you have the following installed:

- Python 3.7+
- [Terraform CLI](https://developer.hashicorp.com/terraform/downloads)
- `graphviz` and its Python bindings:
  ```bash
  sudo apt install graphviz  # Linux
  brew install graphviz      # macOS

  pip install graphviz