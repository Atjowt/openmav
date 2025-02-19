"""
OpenMaverick API for FlightGear
"""

import re
import asyncio
import subprocess
import telnetlib3 as tn

def launch(flightgear_path='fgfs', port=5401) -> None:
    """
    Launches the FlightGear program on the given Telnet port.
    """
    command = [flightgear_path, f'--telnet={port}']
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print('FlightGear executable not found. Check the path or installation')
    except subprocess.CalledProcessError as e:
        print('An error occurred while launching FlightGear:', e)

# TODO: provide a mapping from native python objects to flightgear string parameter names

class FGClient:

    """
    A FlightGear Telnet client.
    Provides easy methods for getting and setting FlightGear parameters.
    """

    def __init__(self, reader: tn.TelnetReader, writer: tn.TelnetWriter) -> None:
        self.reader = reader
        self.writer = writer

    async def get(self, attribute: str):
        """
        Reads the value of an attribute.
        The value is automatically cast to the correct type.
        """
        self.writer.write(b'get /position/altitude-ft\r\n')
        response_bytes = await self.reader.readline()
        response = response_bytes.decode('utf-8')
        # print(response)
        pattern = r'(.*) = \'(.*)\' \((.*)\)' # regular expression, matches expressions of the format '<name> = <value> (<type>)'
        match = re.search(pattern, response)
        if not match: raise Exception('Bad regular expression') # should be unreachable if the pattern isn't wrong
        var_name = match.group(1) # unused (for now)
        var_value = match.group(2)
        var_type = match.group(3)
        match var_type:
            case 'double': return float(var_value)
            case 'none': return None # TODO: better handling for the no-type case

    async def set(self, attribute: str, value) -> None:
        ... # TODO: implement setting of parameters

async def connect(host='127.0.0.1', port=5401) -> FGClient:
    """
    Connect to a running FlightGear instance using host address and port.
    """
    reader, writer = await tn.open_connection(host=host, port=port, encoding=False)
    client = FGClient(reader, writer)
    return client
