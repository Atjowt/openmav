#!/usr/bin/env python

import subprocess
from prompt import prompt

def main():

    path = prompt('Enter FlightGear path', default='fgfs')
    host = prompt('Enter host address', default='127.0.0.1')
    port = prompt('Enter port', default='5500')
    rate = prompt('Enter polling rate (Hz)', default='10')
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
    print('Rate: ', rate, 'Hz')
    print('Args: ', args)

    if prompt('Launch FlightGear?', default='y').lower() == 'y':
        command = [
            path,
            f'--native-fdm=socket,out,{rate},{host},{port},udp',
        ] + args.split()
        subprocess.run(command)

if __name__ == '__main__':
    main()
