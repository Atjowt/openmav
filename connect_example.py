#!/usr/bin/env python

from openmav import Reader, Writer

def main():
    print('Connecting to FlightGear...')
    try:
        reader = Reader(host='localhost', port=5500)
        writer = Writer(host='localhost', port=5400)
    except ConnectionRefusedError:
        print('Connection failed. Is FlightGear running?')
        return
    print('Connected!')
    while True:
        print('Reading data...')
        try:
            data = reader.read()
        except:
            print('Could not read data')
            break
        print('Current altitude is', data.altitude, 'feet')
        data.altitude += 10.0
        print('Sending data...')
        try:
            writer.write(data)
        except:
            print('Could not write data')
            break
    print('Closing...')
    reader.close()

if __name__ == '__main__':
    main()
