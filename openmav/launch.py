from subprocess import Popen

# TODO: add preset launchers, like the F16 fly straight example

class Launcher:

    def aircraft(self, value: str) -> 'Launcher':
        self._aircraft = value
        return self

    def altitude(self, value: int) -> 'Launcher':
        self._altitude = value
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
        self._extra = args
        return self

    def launch(self, path='fgfs'):
        command = [
            path,
            # '--fdm=null',
            f'--aircraft={self._aircraft}',
            f'--altitude={self._altitude}',
            f'--generic=socket,in,{self._input_rate},localhost,{self._input_port},tcp,openmav',
            f'--generic=socket,out,{self._output_rate},localhost,{self._output_port},udp,openmav',
        ] + self._extra
        return Popen(command)

