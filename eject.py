#!/usr/bin/env python

import openmav
import time

def main():
    try:
        reader = openmav.Reader(host='localhost', port=5500)
        writer = openmav.Writer(host='localhost', port=5400)
    except ConnectionRefusedError:
        return
    out_data = openmav.OutData(throttle=0.7, aileron=0.5)
    writer.write(out_data)
    time.sleep(0.5)
    while True:
        in_data = reader.read()
        if abs(in_data.roll) < 0.1:
            break
    out_data.aileron = 0.0
    writer.write(out_data)
    reader.close()
    writer.close()

if __name__ == '__main__':
    main()
