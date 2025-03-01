import re
import asyncio
import subprocess
import telnetlib3 as tn

class Connection:

    """
    A FlightGear Telnet client.
    Provides easy methods for getting and setting FlightGear parameters.
    """

    async def __init__(self, host='127.0.0.1', port=5401) -> None:
        self.reader, self.writer = await tn.open_connection(host=host, port=port, encoding=False)

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
            case 'none': return None # TODO: better handling for the no-type case

    async def set(self, attribute: str, value) -> None:
        ... # TODO: implement setting of parameters
