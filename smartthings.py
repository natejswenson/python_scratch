
from decouple import config
import aiohttp
import pysmartthings

###########################################################################################
#global_vars
###########################################################################################
PAT = config('smart_things_pat')

###########################################################################################
#Main
###########################################################################################
async def main():
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, PAT)
        event = await api.devices()
        for i in range(len(event)):
            device = event[i]
            print(device.name)
            print(device.device_id)
            print(device.capabilities)
            print('-------------------------')
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
