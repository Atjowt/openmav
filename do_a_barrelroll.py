#!/usr/bin/env python

import openmav

# Assuming FlightGear was launched with the options from `launch_example.py`

def main():
    print('Connecting to FlightGear...')
    try:
        reader = openmav.Reader(host='localhost', port=5500)
        writer = openmav.Writer(host='localhost', port=5400)
    except ConnectionRefusedError:
        print('Connection refused. Is FlightGear running?')
        return
    print('Connected!')
    full_turn = 360.0
    num_steps = 80
    delta_turn = full_turn / num_steps
    for step in range(num_steps):
        in_data = reader.read()
        print('Current altitude is', in_data.altitude, 'feet')
        print('Current roll is', in_data.roll, 'degrees')
        out_data = openmav.OutData (
            throttle=0.7,
            roll=in_data.roll+delta_turn
        )
        writer.write(out_data)
    print('Closing...')
    reader.close()
    writer.close()

if __name__ == '__main__':
    main()
