#!/usr/bin/env python

import openmav

def main():

    print('Launching FlightGear...')

    options = openmav.LaunchOptions (
        aircraft=openmav.aircraft.F16_BLOCK_30,
        altitude=5000.0,
        # latitude=59.331754,
        # longitude=18.057119,
        heading=180.0,
        speed=400.0,
        throttle=0.5,
        engine_running=True,
        input=openmav.SocketOptions(port=5400, rate=30),
        output=openmav.SocketOptions(port=5500, rate=30),
    )

    options.args = [
        '--state=cruise',
        '--httpd=5000',
    ]

    _ = openmav.launch(options=options)

if __name__ == '__main__':
    main()
