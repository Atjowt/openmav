"""
OpenMaverick API for FlightGear
"""


def launch(flightgear_path='fgfs', port=5401) -> subprocess.Popen:
    """
    Launches the FlightGear program on the given Telnet port.
    """
    command = [flightgear_path, f'--telnet={port}']
    try:
        return subprocess.Popen(command, stdout=None)
        # subprocess.run(command, shell=False, check=True)
    except FileNotFoundError:
        print('FlightGear executable not found. Check the path or installation')
    except subprocess.CalledProcessError as e:
        print('An error occurred while launching FlightGear:', e)

# TODO: provide a mapping from native python objects to flightgear string parameter names


async def connect(host='127.0.0.1', port=5401) -> FGClient:
    """
    Connect to a running FlightGear instance using host address and port.
    """
    reader, writer = await tn.open_connection(host=host, port=port, encoding=False)
    client = FGClient(reader, writer)
    return client
