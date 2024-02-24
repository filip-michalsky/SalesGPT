# Define shell to use
#SHELL := /bin/bash

# Define Python interpreter
#PYTHON_MAC := python3
#PYTHON_WINDOWS := python

# Define virtual environment directory
VENV := .venv

# Default target executed when no arguments are given to make.
default: test

test:	## run tests with pytest.
	@echo "Running tests..."
	@pytest --cov=salesgpt --cov-report=term-missing --cov-report=html
	@echo "Tests executed."

# Set up the development environment
setup:
	pip install -U pip setuptools
	pip install poetry
	@echo "Poetry installed."
	@echo "Installing project dependencies using Poetry."
	poetry install
	@echo "Dependencies installed."

# Clean up the environment
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	rm -rf SalesGPT
	@echo "Environment cleaned up."

.PHONY: default setup test clean
