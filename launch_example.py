#!/usr/bin/env python

import openmav
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="The program launches FlightGear with the specifiec startup parameters."
    )
    parser.add_argument("--aircraft", type=str, default=openmav.aircraft.F16_BLOCK_30, help="Specifies what aircraft model to use.")
    parser.add_argument("--altitude", type=float, default=7000.0, help="Specifies the initial altitude.")
    parser.add_argument("--latitude", type=float, default=60.8, help="Specifies the initial latitude.")
    parser.add_argument("--longitude", type=float, default=17.1, help="Specifies the initial longitude.")
    parser.add_argument("--heading", type=float, default=180.0, help="Specifies the initial heading (in degrees).")
    parser.add_argument("--speed", type=float, default=400.0, help="Specifies the initial speed.")
    args = parser.parse_args()

    print('Launching FlightGear...')

    launch_options = openmav.LaunchOptions (
        aircraft=args.aircraft,
        altitude=args.altitude,
        latitude=args.latitude,
        longitude=args.longitude,
        heading=args.heading,
        speed=args.speed,
        input=openmav.SocketOptions(port=5400, rate=10),
        output=openmav.SocketOptions(port=5500, rate=10),
    )

    launch_options.args = [
        f'--prop:/controls/engines/engine/throttle=0.7',
        f'--prop:/engines/engine[0]/running=true',
        f'--state=cruise',
    ]

    _ = openmav.launch(options=launch_options)

if __name__ == '__main__':
    main()
