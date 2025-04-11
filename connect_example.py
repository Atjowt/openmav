#!/usr/bin/env python

import openmav

# Assuming FlightGear was launched with the options from `launch_example.py`

def main():
    print('Connecting to FlightGear...')
    try:
        reader = openmav.Reader(port=5500)
    except ConnectionRefusedError:
        print('Connection refused. Is FlightGear running?')
        return
    print('Connected!')
    while in_data := reader.read():
        print('Current altitude is', in_data.altitude, 'feet')
        print('Current roll is', in_data.roll, 'degrees')
    print('Closing...')
    reader.close()

if __name__ == '__main__':
    main()
