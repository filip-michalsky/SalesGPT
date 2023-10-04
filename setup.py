import os

from setuptools import find_packages, setup

base_dir = os.path.dirname(os.path.abspath(__file__))


def get_long_description():
    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, encoding="utf-8") as readme_file:
        return readme_file.read()


def get_project_version():
    version_path = os.path.join(base_dir, "salesgpt", "version.py")
    version = {}
    with open(version_path, encoding="utf-8") as fp:
        exec(fp.read(), version)
    return version["__version__"]


def get_requirements(path):
    with open(path, encoding="utf-8") as requirements:
        return [requirement.strip() for requirement in requirements]


install_requires = get_requirements(os.path.join(base_dir, "requirements.txt"))

setup(
    name="salesgpt",
    version=get_project_version(),
    license="Apache 2.0",
    description="SalesGPT - Your Context-Aware AI Sales Assistant",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Filip Michalsky",
    url="https://github.com/filip-michalsky/SalesGPT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="openai sales gpt autonomous agi",
    python_requires=">=3.10",
    install_requires=install_requires,
    extras_require={
        "dev": [
            "black==23.*",
            "flake8==6.*",
            "isort==5.*",
            "pytest==7.*",
            "pytest-asyncio==0.21.*",
        ],
    },
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
)
