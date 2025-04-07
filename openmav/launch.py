from subprocess import Popen
import argparse

# TODO: add preset launch options

class SocketOptions:
    def __init__(self, port=5400, rate=10) -> None:
        self.port = port
        self.rate = rate

class LaunchOptions:

    def __init__(self,
        aircraft: str | None = None,
        altitude: float | None = None,
        heading: float | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        speed: float | None = None,
        throttle: float | None = None,
        engine_running: bool | None = None,
        input: SocketOptions | None = None,
        output: SocketOptions | None = None,
        args: list[str] | None = None,
    ) -> None:
        self.aircraft = aircraft
        self.altitude = altitude
        self.heading = heading
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.throttle = throttle
        self.engine_running = engine_running
        self.input = input
        self.output = output
        self.args = args


def read_launch_options(options: LaunchOptions) -> LaunchOptions:
    parser = argparse.ArgumentParser(description="The program launches FlightGear with the specified startup parameters.")

    parser.add_argument("--aircraft", type=str, default=options.aircraft, help="Specifies what aircraft model to use.")
    parser.add_argument("--altitude", type=float, default=options.altitude, help="Specifies the initial altitude.")
    parser.add_argument("--latitude", type=float, default=options.latitude, help="Specifies the initial latitude.")
    parser.add_argument("--longitude", type=float, default=options.longitude, help="Specifies the initial longitude.")
    parser.add_argument("--heading", type=float, default=options.heading, help="Specifies the initial heading (in degrees).")
    parser.add_argument("--speed", type=float, default=options.speed, help="Specifies the initial speed.")
    args = parser.parse_args()

    options.aircraft = args.aircraft
    options.altitude = args.altitude
    options.latitude = args.latitude
    options.longitude = args.longitude
    options.heading = args.heading
    options.speed = args.speed

    return options


def launch(path: str = 'fgfs', options: LaunchOptions | None = None) -> Popen[bytes]:
    command = [path]
    if options is not None:
        if options.aircraft is not None: command.append(f'--aircraft={options.aircraft}')
        if options.altitude is not None: command.append(f'--altitude={options.altitude}')
        if options.heading is not None: command.append(f'--heading={options.heading}')
        if options.latitude is not None: command.append(f'--lat={options.latitude}')
        if options.longitude is not None: command.append(f'--lon={options.longitude}')
        if options.speed is not None: command.append(f'--vc={options.speed}')
        if options.throttle is not None: command.append(f'--prop:/controls/engines/engine[0]/throttle={options.throttle}')
        if options.engine_running is not None: command.append(f'--prop:/engines/engine[0]/running={str(options.engine_running).lower()}')
        if options.input is not None: command.append(f'--generic=socket,in,{options.input.rate},localhost,{options.input.port},udp,openmav')
        if options.output is not None: command.append(f'--generic=socket,out,{options.output.rate},localhost,{options.output.port},udp,openmav')
        if options.args is not None: command.extend(options.args)
    return Popen(command)

