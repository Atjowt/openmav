#!/usr/bin/env python

from openmav import Aircraft, Launcher

def main():

    latitude = 60.8
    longitude = 17.1
    heading = 180
    speed = 400

    # TODO: make these available as launch options!!

    args = [
        f'--heading={heading}',
        f'--lat={latitude}',
        f'--lon={longitude}',
        f'--vc={speed}',
        f'--prop:/controls/engines/engine/throttle=0.7',
        f'--prop:/engines/engine[0]/running=true',
        f'--state=cruise',
    ]

    print('Launching FlightGear...')

    process = Launcher() \
        .input(port=5400, rate=2) \
        .output(port=5500, rate=10) \
        .aircraft(Aircraft.F16_BLOCK_30) \
        .altitude(7000) \
        .extra(args) \
        .launch()

    process.wait()

if __name__ == '__main__':
    main()
