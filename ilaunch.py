#!/usr/bin/env python

"""
Interactive FlightGear launcher.
"""

import subprocess

def prompt(msg: str, default='') -> str:
    try:
        if default:
            inp = input(f'{msg} (default={default}): ')
        else:
            inp = input(f'{msg}: ')
    except EOFError:
        print('Exiting...')
        exit()
    if not inp:
        inp = default
    return inp

def args_f16_airborne(latitude, longitude, altitude, speed) -> list[str]:
    return [
        
    ]

def main():

    while True:
        path = prompt('Enter FlightGear path', default='fgfs')
        host = prompt('Enter host address', default='127.0.0.1')
        port = prompt('Enter port', default='5500')
        rate = prompt('Enter polling rate', default='10')
        args = prompt('Enter additional args', default=f'''
        --aircraft=f16-block-30
        --altitude=15000
        --lat=59.354
        --lon=17.939
        --vc=400
        --prop:/controls/engines/engine/throttle=0.7
        --prop:/engines/engine[0]/running=true
        --state=cruise''')

        print('Path:', path)
        print('Host:', host)
        print('Port: ', port)
        print('Rate: ', rate)
        print('Args: ', args)

        if prompt('OK?', default='y').lower() == 'y':
            break

    command = [
        path,
        f'--native-fdm=socket,out,{rate},{host},{port},udp',

    ] + args.split()

    print('Launching FlightGear...')

    subprocess.run(command)

if __name__ == '__main__':
    main()
