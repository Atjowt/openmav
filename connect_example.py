#!/usr/bin/env python

import openmav

# Assuming FlightGear was launched with the options from `launch_example.py`

def main():
    print('Connecting to FlightGear...')
    try:
        reader = openmav.Reader(port=5500)
        writer = openmav.Writer(port=5400)
    except ConnectionRefusedError:
        print('Connection refused. Is FlightGear running?')
        return
    print('Connected!')
    nav = openmav.Navigator(reader, writer)
    print('Right')
    nav.roll_towards(+90.0, 4.0, 10.0, 16.0, 100)
    print('Left')
    nav.roll_towards(-90.0, 4.0, 10.0, 16.0, 100)
    nav.roll_towards(0.0, 4.0, 10.0, 16.0, 100)
    print('Up')
    nav.pitch_towards(+45.0, 16.0, 10.0, 16.0, 100)
    print('Down')
    nav.pitch_towards(-45.0, 16.0, 10.0, 16.0, 100)
    nav.pitch_towards(0.0, 16.0, 10.0, 16.0, 100)
    print('Done')
    reader.close()
    writer.close()

if __name__ == '__main__':
    main()
