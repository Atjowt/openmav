# OpenMaverick

## Setting up and running the examples
OpenMav uses sockets to communicate with FlightGear. We define a custom data protocol through an XML file, `protocol/openmav.xml`, which **must be copied locally** to `$FG_ROOT/Protocol` for FlightGear to recognize it on launch.
With the protocol installed, you should be able to run the examples `launch_example.py` and `connect_example.py`.
There is also a simple GUI application under `graphics.py` which allows for running some simple preset scripts and also displays current flight parameters. 
