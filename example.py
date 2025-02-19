import asyncio
import openmav

async def main():
    """
    Example of getting flight altitude parameter
    """
    print('Connecting...')
    client = await openmav.connect()
    print('Connected!')
    altitude_ft = await client.get('/position/altitude-ft')
    print('Current altitude is', altitude_ft, 'ft')

if __name__ == '__main__':
    asyncio.run(main())
