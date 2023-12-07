# Define shell to use
#SHELL := /bin/bash

# Define Python interpreter
#PYTHON_MAC := python3
#PYTHON_WINDOWS := python

# Define virtual environment directory
VENV := env

# Default target executed when no arguments are given to make.
default: test

test:	## run tests with pytest.
	@echo "Running tests..."
	@pytest --cov=salesgpt --cov-report=term-missing --cov-report=html
	@echo "Tests executed."

# Set up the development environment
setup: install_poetry clone_repo install_dependencies

# Install Poetry for dependency management
install_poetry:
	pip install -U pip setuptools
	pip install poetry
	@echo "Poetry installed."

# Clone the GitHub repository
clone_repo:
	git clone https://github.com/filip-michalsky/SalesGPT.git
	@echo "Repository cloned."

# Install project dependencies using Poetry
install_dependencies:
	cd SalesGPT && poetry install
	@echo "Dependencies installed."
	
# Clean up the environment
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	rm -rf SalesGPT
	@echo "Environment cleaned up."

.PHONY: default setup install_poetry clone_repo install_dependencies test clean

