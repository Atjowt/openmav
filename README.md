# OpenMaverick

## Sockets
This implementation uses a UDP socket to get data from FlightGear, which offers much higher bandwidth.
For now it is only possible to receive data, not send.
The plan is to have two methods of sending data:
- A fast UDP socket for sending over the entire property tree at once - would be useful to an AI for sending data rapidly
- A reliable Telnet/TCP socket for setting individual properties - guarantess that properties are set, but at the cost of speed.

# Running
The API and client is currently written in C. To build and run it, type `make run`.
There is also a helper script `ilaunch.py` which steps you through launching FlightGear with the right arguments.
