# OpenMaverick

## Setting up the Python virtual environment
In the root of the project, create a directory named `venv` to hold the virtual environment (`mkdir venv/`).
Create the virtual environment inside this directory by running `python -m venv venv/`.
Enter the virtual environment by running (Linux) `source venv/bin/activate` or (Windows) `venv/Scripts/activate`.
This will activate the virtual environment for your current shell session. You should now see the text "(venv)" written in your terminal. You may leave the environment at any time by writing `deactivate`.
Finally, install the flightgear-python package by running `pip3 install flightgear-python --include-deps`.

## Running the examples
First set up the virtual environment, if you haven't already.
Running an example should be as simple as writing `python3 /path/to/example.py`.

