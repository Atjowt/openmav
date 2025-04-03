#!/usr/bin/env python

from openmav import Aircraft, Launcher

def main():

    args = [
        f'--prop:/controls/engines/engine/throttle=0.7',
        f'--prop:/engines/engine[0]/running=true',
        f'--state=cruise',
    ]

    print('Launching FlightGear...')

    Launcher() \
        .input(port=5400, rate=10) \
        .output(port=5500, rate=10) \
        .aircraft(Aircraft.F16_BLOCK_30) \
        .altitude(7000) \
        .latitude(60.8) \
        .longitude(17.1) \
        .heading(180) \
        .speed(400) \
        .extra(args) \
        .launch()

if __name__ == '__main__':
    main()
