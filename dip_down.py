#!/usr/bin/env python

import openmav
import time

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

    out_data.elevator = 0.8
    writer.write(out_data)

    time.sleep(1.0)

    out_data.elevator = -0.4
    writer.write(out_data)

    time.sleep(2.0)

    out_data.elevator = start_data.elevator
    writer.write(out_data)

    reader.close()
    writer.close()

if __name__ == '__main__':
    main()
