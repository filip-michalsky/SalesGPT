---
sidebar_position: 2

---
# Setup

## Install

Make sure you have a **python &gt;=3.8,&lt;3.12**:

Create a virtual environment at a location on your computer. We use the generic "env" name for our virtual environment in the setup. You can rename this, but make sure to then use this name later when working with the environment (also rename the VENV variable in the Makefile accordingly to be able to use make commands successfully after cloning our repository):

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

To deactivate a virtual environment after you have stopped using it simply run: `deactivate`

Clone the SalesGPT Github repository: 

`git clone https://github.com/filip-michalsky/SalesGPT.git`

Navigate to the repository and in case you used a different venv name rename the VENV variable in the Makefile: 

`cd SalesGPT`



If you simply want to work with SalesGPT as an end user without local changes you can install from PyPI using: 

`pip install salesgpt`

If you want to work on your own version of SalesGPT or contribute to our open-source version install by activating your virtual environment as aforementioned and then run: 

`make setup`

For more detailed installation steps along with the reasons for doing each please visit CONTRIBUTING.md

Finally, for use of SalesGPT create an `.env` file just as our `.env.example` and put your API keys there by specifying a new line just as we have done.