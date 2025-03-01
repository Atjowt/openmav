#!/usr/bin/env python

import openmav
from prompt import prompt

def main():
    host = prompt('Enter host address', default='127.0.0.1')
    port = int(prompt('Enter port', default='5500'))
    print('Connecting...')
    client = openmav.ConnectionUDP(host, port)
    print('Connected!')
    while data := client.receive():
        print()
        print(f'Current Altitude: {data.altitude:.5f} m')
        print(f'Current Latitude: {data.latitude:.5f} rad')
        print(f'Current Longitude: {data.longitude:.5f} rad')
    print('Disconnected.')

if __name__ == '__main__':
    main()
