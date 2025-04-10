#!/usr/bin/env python

import openmav

def main():

    reader = openmav.Reader(host='localhost', port=5500)
    writer = openmav.Writer(host='localhost', port=5400)

    start_data = reader.read()

    out_data = openmav.OutData (
        throttle=start_data.throttle,
        aileron=start_data.aileron,
        elevator=start_data.elevator,
        rudder=start_data.rudder,
    )

    out_data.aileron = 0.8 # tilt the aircraft
    out_data.throttle *= 2.0 # double the throttle!

    print('Barrelroll!')
    writer.write(out_data)

    while True:
        in_data = reader.read()
        print('Roll is ', in_data.roll, 'degrees')
        if abs(in_data.roll - start_data.roll) > 130.0:
            break

    print('Upside-down')

    while True:
        in_data = reader.read()
        print('Roll is ', in_data.roll, 'degrees')
        if abs(in_data.roll - start_data.roll) < 30.0:
            break

    print('Done')
    out_data.aileron = start_data.aileron
    out_data.throttle = start_data.throttle
    writer.write(out_data)

    reader.close()
    writer.close()

if __name__ == '__main__':
    main()
