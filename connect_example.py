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
    while in_data := reader.read():
        print('Current altitude is', in_data.altitude, 'feet')
        print('Current roll is', in_data.roll, 'degrees')
        out_data = openmav.OutData (
            throttle=0.7,
        )
        writer.write(out_data)
    print('Closing...')
    reader.close()
    writer.close()

if __name__ == '__main__':
    main()
