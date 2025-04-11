#!/usr/bin/env python

import openmav

def main():

    reader = openmav.Reader()
    writer = openmav.Writer()

    in_data = reader.read()

    out_data = openmav.OutData.from_indata(in_data)

    out_data.aileron = 0.8 # tilt the aircraft
    out_data.throttle *= 2.0 # double the throttle!

    print('Barrelroll!')

    writer.write(out_data)

    threshold = 5.0

    initial_roll = in_data.roll

    # wait until rolled 180'
    while True:
        in_data = reader.read()
        print('Roll is ', in_data.roll, 'degrees')
        if abs(in_data.roll - initial_roll) > 180.0 - threshold:
            break

    print('Upside-down')

    # wait until rolled another 180'
    while True:
        in_data = reader.read()
        print('Roll is ', in_data.roll, 'degrees')
        if abs(in_data.roll - initial_roll) < threshold:
            break

    # stabilize rotation
    print('Stabilizing')
    for _ in range(90):
        in_data = reader.read()
        out_data = openmav.OutData.from_indata(in_data)
        delta_roll = initial_roll - in_data.roll
        print('Delta roll: ', delta_roll)
        out_data.aileron = 10.0 * (delta_roll / 360.0) # tilt ailerons to counteract roll
        writer.write(out_data)

    print('Done')

    reader.close()
    writer.close()

if __name__ == '__main__':
    main()
