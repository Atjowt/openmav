import subprocess
import asyncio
import telnetlib3 as tn

def launch(flightgear_path='fgfs', port=5401) -> None:
    command = [flightgear_path, f'--telnet={port}']
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print('FlightGear executable not found. Check the path or installation')
    except subprocess.CalledProcessError as e:
        print('An error occurred while launching FlightGear:', e)

class FGClient:
    def __init__(self, reader: tn.TelnetReader, writer: tn.TelnetWriter) -> None:
        self.reader = reader
        self.writer = writer

    async def send(self, command: str, timeout=5) -> str:
        print(f"Sending command: {command}")  # Debugging
        self.writer.write(command + '\n')
        try:
            # Wait for data with a timeout
            response = await asyncio.wait_for(self.reader.read(1024), timeout)
            print(f"Raw response: {response}")  # Debugging
            return response.strip()
        except asyncio.TimeoutError:
            print("Timeout: No response received from FlightGear.")
            return ""

    async def get_altitude(self) -> float:
        altitude_str = await self.send('get /position/altitude-ft')
        if altitude_str:
            try:
                altitude_ft = float(altitude_str)
                return altitude_ft
            except ValueError:
                print(f"Failed to parse altitude: {altitude_str}")
        return 0.0  # Default value if parsing fails

async def connect(host='127.0.0.1', port=5401) -> FGClient:
    reader, writer = await tn.open_connection(host=host, port=port)
    client = FGClient(reader, writer)
    await client.send('data')  # Initialize the connection
    return client

async def main():
    # Launch FlightGear (you can comment this out if FlightGear is already running)
    # launch()

    # Connect to FlightGear
    client = await connect()

    # Get altitude
    altitude = await client.get_altitude()
    print(f"Current altitude: {altitude} ft")

    # You can add more commands here to interact with FlightGear

if __name__ == "__main__":
    asyncio.run(main())
