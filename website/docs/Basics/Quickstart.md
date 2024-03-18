---
sidebar_position: 2

---


# Deployment Guide

## Run an Example AI Sales agent
If you used a local installation of SalesGPT skip the next two steps and directly run the run.py script: 

`git clone https://github.com/filip-michalsky/SalesGPT.git`

`cd SalesGPT`

`python run.py --verbose True --config examples/example_agent_setup.json`

from your terminal.

## Test your setup

1. Activate your environment as described above. (run `source env/bin/activate` on Unix-like systems and `.\env\Scripts\activate` on Windows. Replace *env* with the name of your virtual environment)
2. cd `SalesGPT`      If you haven't already navigated to the SalesGPT home directory
3. `make test`

All tests should pass. Warnings can be ignored.

## Uninstall SalesGPT

To delete the virtual environment you used for SalesGPT programming and your SalesGPT repository from your system navigate to the directory where you installed your virtual environment and cloned SalesGPT and run: 
`make clean`

## Deploy

We have a SalesGPT deployment demo via FastAPI.

Please refer to [README-api.md](https://github.com/filip-michalsky/SalesGPT/blob/main/README-api.md) for instructions!