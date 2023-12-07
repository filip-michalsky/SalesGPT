# Project Setup Instructions

## Introduction

This CONTRIBUTING document provides instructions for setting up your development environment for our project. It includes steps for creating a virtual environment, installing Python, using Poetry for dependency management, and cloning the project from GitHub and running a trial of our project.

## Why Use a Virtual Environment?

A virtual environment is a self-contained directory that holds a specific version of Python and various packages. Using a virtual environment allows you to manage dependencies for different projects separately, avoiding conflicts and ensuring consistency across development setups.

## Prerequisites

- Access to a command-line interface (Terminal for Mac, Command Prompt or PowerShell for Windows)
- Internet connection

### 1. Installing Python

If you do not have Python 3.8 or higher, or would like a separate Python version for this project, follow these steps to download and install it. You can download and install a new version of Python without overwriting your current version. Python supports having multiple versions installed on the same system.

#### For Windows:

- Download the Installer: Go to the official Python website and download the installer for the new Python version.
- Run the Installer: Launch the installer. Be sure to select the option to “Customize installation”.
- Choose a Different Directory: During the installation process, specify a different installation directory than the one used by your current Python version.
- Update the Environment Variables (Optional): If you want to use the new Python version as the default in your command line, you can update the PATH environment variable to point to the new installation.

#### For Mac:

- Download Python: Visit the official Python website and download the desired Python versions.
- Install Python: Open the downloaded installer and follow the instructions.
- Verify Installations: Open Terminal and check the installations by typing `python3.x --version`, where `3.x` corresponds to the version numbers you've installed.

### 2. Creating a Virtual Environment

#### For Windows:

- Open Command Prompt or PowerShell.
- Navigate to your project directory: `cd path\to\your\project`
- Create a virtual environment: `python -m venv env`
- Activate the virtual environment: `.\env\Scripts\activate`

#### For Mac:

- Open Terminal.
- Navigate to your project directory: `cd path/to/your/project`
- Create a virtual environment: `python3 -m venv env`
- Activate the virtual environment: `source env/bin/activate`

### 3. Installing Poetry

Poetry is a tool for dependency management and packaging in Python.

#### For Windows and Mac:

- Ensure your virtual environment is active.
- Make sure you have the latest version of pip using: `pip install -U pip setuptools`
- Install Poetry by running: `pip install poetry`

### 4. Cloning the GitHub Repository

To clone the project repository:

- Ensure git is installed on your system. If not, download and install from git-scm.com.
- Navigate to the directory where you want to clone the repository.
- Clone the repository: `git clone https://github.com/filip-michalsky/SalesGPT.git`.

### 5. Installing Dependencies with Poetry

Dependencies must be installed to ensure all necessary libraries and packages are available for the project.

#### For Windows and Mac:

- Run `poetry install` in the project directory.
- This command reads the `pyproject.toml` file and installs all listed dependencies.

### 6. Setting Up Environment Variables

Environment variables, including API keys, are crucial for the project's configuration and security.

#### For Windows and Mac:

- Create a `.env` file in the project root.
- Use the `.env.example` file as a template.
- Add your API keys and other necessary variables, following the example's format.
- This step ensures that your personal and project-specific configurations are correctly set up.

### 7. Running Tests with Pytest

Running tests is essential for ensuring the integrity and functionality of the code.

#### For Windows and Mac:

- Execute `make test` in the command line.
- This command runs all test cases in the project.
- Ensure there are no failures; warnings can be ignored.
- Successful test runs indicate that the setup and project code are functioning correctly.

## Conclusion

You now have a complete setup for developing the project, including dependency management and testing. Always activate the virtual environment before working on the project.
