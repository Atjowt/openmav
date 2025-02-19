# OpenMaverick

## Cloning and working Git
1. To begin, clone the repository using `git clone <repository-address>`. If you are using HTTPS this would look like `git clone https://github.com/Atjowt/pvk24.git`.
2. Whenever you want to make some changes on your local machine, start by doing a `git pull --rebase` to avoid unnecessary merge conflicts later down the line.
3. Make sure to provide a reasonable commit message for your changes, see `git log` for examples of previous commits.
4. When you are done making your changes, verify that **the program still runs**, and then push your changes with `git push`.

## Installing and setting up FlightGear
TODO

## Setting up the Python virtual environment
1. In the root of the project, create a directory named `venv` to hold the virtual environment (`mkdir venv/`).
2. Create the virtual environment inside this directory by running `python -m venv venv/`.
3. Enter the virtual environment by running (Linux) `source venv/bin/activate` or (Windows) `venv/Scripts/activate`. This will activate the virtual environment for your current shell session. You should now see the text "(venv)" written in your terminal. You may leave the environment at any time by writing `deactivate`.

## Installing required Python packages
First set up and activate the virtual environment, if you haven't already done so.
- Install the 'flightgear-python' package by running ```pip3 install flightgear-python --include-deps```.
- Install the 'telnetlib3' package by running ```pip3 install telnetlib3```.

## Running the example code
Once you have installed all required packages, you are ready to launch an example.
Running an example should be as simple as writing `python3 /path/to/example.py`.

