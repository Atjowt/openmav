import asyncio
import openmav

async def main():
    """
    Example of connecting to a FlightGear instance and getting flight parameters
    """
    print('Connecting...')
    client = await openmav.connect()
    print('Connected!')
    altitude_ft = await client.get('/position/altitude-ft')
    print('Current altitude is', altitude_ft, 'ft')
    longitude_deg = await client.get('/position/longitude-deg')
    print('Current longitude is', longitude_deg, 'deg')

if __name__ == '__main__':
    asyncio.run(main())
