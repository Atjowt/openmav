from subprocess import Popen

# TODO: add preset launchers, like the F16 fly straight example
# TODO: make command include parameters only if they are specified

class Launcher:

    def __init__(self) -> None:
        self._aircraft = None
        self._altitude = None
        self._heading = None
        self._latitude = None
        self._longitude = None
        self._speed = None
        self._input_port = None
        self._input_rate = None
        self._output_port = None
        self._output_rate = None
        self._extra_args = None

    def aircraft(self, value: str) -> 'Launcher':
        self._aircraft = value
        return self

    def altitude(self, value: float) -> 'Launcher':
        self._altitude = value
        return self

    def heading(self, value: float) -> 'Launcher':
        self._heading = value
        return self

    def latitude(self, value: float) -> 'Launcher':
        self._latitude = value
        return self

    def longitude(self, value: float) -> 'Launcher':
        self._longitude = value
        return self

    def speed(self, value: float) -> 'Launcher':
        self._speed = value
        return self

    def input(self, port: int, rate: int) -> 'Launcher':
        self._input_port = port
        self._input_rate = rate
        return self

    def output(self, port: int, rate: int) -> 'Launcher':
        self._output_port = port
        self._output_rate = rate
        return self

    def extra(self, args: list[str]) -> 'Launcher':
        self._extra_args = args
        return self

    def launch(self, path='fgfs'):
        command = [
            path,
            f'--aircraft={self._aircraft}' if self._aircraft is not None else '',
            f'--altitude={self._altitude}' if self._altitude is not None else '',
            '--fdm=null' if self._input_port is not None else '',
            f'--generic=socket,in,{self._input_rate},localhost,{self._input_port},tcp,openmav' if self._input_port is not None else '',
            f'--generic=socket,out,{self._output_rate},localhost,{self._output_port},udp,openmav' if self._output_port is not None else '',
            f'--heading={self._heading}' if self._heading is not None else '',
            f'--lat={self._latitude}' if self._latitude is not None else '',
            f'--lon={self._longitude}' if self._latitude is not None else '',
            f'--vc={self._speed}' if self._speed is not None else '',
        ]
        if self._extra_args is not None:
            command.extend(self._extra_args)
        return Popen(command)

