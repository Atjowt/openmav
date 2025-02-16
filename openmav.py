import subprocess

# TODO: make this not suck


# TODO: provide native fields/functions for getting and settings arguments
class FlightEnvironment:


    def __init__(self, args=None) -> None:
        self._args: list[str] = args or []


    def add_arg(self, arg: str) -> None:
        self._args.append(arg)


    def get_args(self) -> list[str]:
        return self._args


    def simple(latitude: float, longitude: float, altitude: float,
               heading: float, speed: float) -> 'FlightEnvironment':

        env = FlightEnvironment()

        env.add_arg("--aircraft=f16-block-30")
        env.add_arg(f"--altitude={altitude}")
        env.add_arg(f"--lat={latitude}")
        env.add_arg(f"--lon={longitude}")
        env.add_arg(f"--vc={speed}")
        env.add_arg("--prop:/controls/engines/engine/throttle=0.7")
        env.add_arg("--prop:/engines/engine[0]/running=true")
        env.add_arg("--state=cruise")
        env.add_arg("--telnet=5401")

        return env


class OpenMav:


    def __init__(self, flightgear_path="fgfs") -> None:
        self.flightgear_path: str = flightgear_path
        self.loaded_environment: FlightEnvironment = None


    def load(self, environment: FlightEnvironment) -> None:
        self.loaded_environment = environment


    def launch(self) -> None:

        if self.loaded_environment is None:
            raise Exception("No flight environment loaded!")

        environment_args = self.loaded_environment.get_args()
        launch_command = [self.flightgear_path] + environment_args

        try:
            subprocess.run(launch_command, check=True)
        except FileNotFoundError:
            print("FlightGear executable not found. Check the path or installation.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while launching FlightGear: {e}")

