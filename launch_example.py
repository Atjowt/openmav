#!/usr/bin/env python

import openmav

def main():
    print('Launching FlightGear...')

    launch_options = openmav.LaunchOptions (
        aircraft=openmav.aircraft.F16_BLOCK_30,
        altitude=7000.0,
        latitude=60.8,
        longitude=17.1,
        heading=180.0,
        speed=400.0,
        input=openmav.SocketOptions(port=5400, rate=10),
        output=openmav.SocketOptions(port=5500, rate=10),
    )

    launch_options.args = [
        f'--prop:/controls/engines/engine/throttle=0.7',
        f'--prop:/engines/engine[0]/running=true',
        f'--state=cruise',
    ]

    launch_options = openmav.read_launch_options(launch_options) # reads launch options from the command line when starting program

    _ = openmav.launch(options=launch_options)

if __name__ == '__main__':
    main()
