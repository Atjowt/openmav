from subprocess import Popen

# TODO: add preset launchers, like the F16 fly straight example
# TODO: make command include parameters only if they are specified

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
        self.input = input
        self.output = output
        self.args = args

def launch(path: str = 'fgfs', options: LaunchOptions | None = None) -> Popen[bytes]:
    command = [path]
    if options is not None:
        if options.aircraft is not None: command.append(f'--aircraft={options.aircraft}')
        if options.altitude is not None: command.append(f'--altitude={options.altitude}')
        if options.heading is not None: command.append(f'--heading={options.heading}')
        if options.latitude is not None: command.append(f'--lat={options.latitude}')
        if options.longitude is not None: command.append(f'--lon={options.longitude}')
        if options.speed is not None: command.append(f'--vc={options.speed}')
        if options.input is not None: command.append(f'--generic=socket,in,{options.input.rate},localhost,{options.input.port},udp,openmav')
        if options.output is not None: command.append(f'--generic=socket,out,{options.output.rate},localhost,{options.output.port},udp,openmav')
        if options.args is not None: command.extend(options.args)
    return Popen(command)

