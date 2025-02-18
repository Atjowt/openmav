import openmav
import asyncio

async def main():
    # Launch FlightGear (you can comment this out if FlightGear is already running)
    # openmav.launch()

    # Connect to FlightGear
    client = await openmav.connect()

    # Get altitude
    altitude = await client.get_altitude()
    print(f"Current altitude: {altitude} ft")

    # You can add more commands here to interact with FlightGear

if __name__ == "__main__":
    asyncio.run(main())
