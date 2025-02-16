# OpenMaverick

## Setting up the Python virtual environment
In the root of the project, create a directory to hold the virtual environment (e.g. `mkdir venv`).
Create the virtual environment by running `python -m venv /path/to/venv` (e.g. `python -m venv venv`).
Enter the virtual environment by running (Linux) `source venv/bin/activate` or (Windows) `venv/Scripts/activate`.
This will activate the virtual environment for your current shell session. You should see the text "(venv)" written in your terminal.
You are now in the virtual environment, and you can leave the environment at any time by writing `deactivate`.
Finally install the `flightgear-python` package by running `pip3 install flightgear-python --include-deps`.

## Running the examples
First set up the virtual environment, if you haven't already.
Running an example should be as simple as typing `python3 /path/to/example.py` (e.g. `python3 examples/simple.py`).

