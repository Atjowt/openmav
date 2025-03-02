#!/usr/bin/env python

from openmav import Reader

def main():
    print('Connecting to FlightGear...')
    try:
        reader = Reader(host='localhost', port=5500)
    except ConnectionRefusedError:
        print('Connection failed. Is FlightGear running?')
        return
    print('Connected!')
    while data := reader.read():
        print('Current altitude is', data.altitude, 'feet')
    reader.close()

if __name__ == '__main__':
    main()
