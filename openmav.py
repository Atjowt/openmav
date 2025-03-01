"""
OpenMaverick API for FlightGear
"""

import re
import asyncio
import subprocess
import telnetlib3 as tn

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
        self.writer.write(f'get {attribute}\r\n'.encode())
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
            case 'string': return str(var_value)
            case 'double': return float(var_value)
            case 'bool': return var_value == 'true'
            case 'none': return None # TODO: better handling for the no-type case

    async def set(self, attribute: str, value) -> None:
        """
        Sets the value of an attribute.
        The input value is validated to ensure it matches the expected type.
        """
        attribute_value = await self.get(attribute)
        
        if isinstance(attribute_value, float) and isinstance(value, (int, float)):
            self.writer.write(f'set {attribute} {value}\r\n'.encode())
        elif isinstance(attribute_value, str) and isinstance(value, str):
            self.writer.write(f'set {attribute} {value}\r\n'.encode())
        elif isinstance(attribute_value, bool) and isinstance(value, bool):
            self.writer.write(f"set {attribute} {1 if value else 0}\r\n".encode())
        else:
            raise TypeError(f"Type mismatch: Expected {type(attribute_value).__name__}, got {type(value).__name__}")
        # TODO better handling for the no-type case
        
        # Clear buffer
        await self.reader.readline()

async def connect(host='127.0.0.1', port=5401) -> FGClient:
    """
    Connect to a running FlightGear instance using host address and port.
    """
    reader, writer = await tn.open_connection(host=host, port=port, encoding=False)
    client = FGClient(reader, writer)
    return client
