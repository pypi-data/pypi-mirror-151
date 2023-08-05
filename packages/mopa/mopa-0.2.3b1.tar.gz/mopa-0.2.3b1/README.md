# mopa
Library for interactive multi-objective power amplifier design

# I. Installation
1. Download [Python](https://www.python.org/downloads/) and ensure you can activate it from your terminal by running `$ python --version` 
2. Install the test verson of mopa using `$ pip install mopa`
3. To check that installation is successful `$ pip show mopa`

# II. Dashboard on Local Machine
mopa now includes the ability to be used as an interactive dashboard!
1. Run python on the command line by running `$ python`
2. Import mopa `>>> import mopa`
3. Create a dashboard `>>> app = mopa.app.create_dashboard()`
4. Run the dashboard `>>> app.run_server()`
