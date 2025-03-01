import asyncio
import openmav

async def main():
    """
    Example of connecting to a FlightGear instance and setting flight parameters
    Note that some values can't be changed if autopilot is activated
    """
    print('Connecting...')
    client = await openmav.connect()
    print('Connected!')
    
    await client.set('/position/latitude-deg', 60.8)
    await client.set('/position/longitude-deg', 17.1)
    await client.set('/position/altitude-ft', 10000)
    await client.set('/orientation/heading-deg', 180)
    await client.set('/velocities/airspeed-kt', 400)
    await client.set('/engines/engine[0]/running', True)

    latitude = await client.get('/position/latitude-deg')
    longitude = await client.get('/position/longitude-deg')
    altitude_ft = await client.get('/position/altitude-ft')
    heading = await client.get('/orientation/heading-deg')
    airspeed_kt = await client.get('/velocities/airspeed-kt')
    engine0 = await client.get('/engines/engine[0]/running')
    
    print('Current latitude is', latitude, 'deg')
    print('Current longitude is', longitude, 'deg')
    print('Current altitude is', altitude_ft, 'ft')
    print('Current heading is', heading, 'deg')
    print('Current airspeed is', airspeed_kt, 'kt')
    print('Engine[0] running: ', engine0)

if __name__ == '__main__':
    asyncio.run(main())