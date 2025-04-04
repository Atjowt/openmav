#!/usr/bin/env python

from openmav import Reader, Writer

# Assuming FlightGear was launched with the options from `launch_example.py`

def main():
    print('Connecting to FlightGear...')
    try:
        reader = Reader(host='localhost', port=5500)
        writer = Writer(host='localhost', port=5400)
    except ConnectionRefusedError:
        print('Connection refused. Is FlightGear running?')
        return
    print('Connected!')
    while data := reader.read():
        print('Current altitude is', data.altitude, 'feet')
        data.altitude += 10.0
        writer.write(data)
    print('Closing...')
    reader.close()
    writer.close()

if __name__ == '__main__':
    main()
