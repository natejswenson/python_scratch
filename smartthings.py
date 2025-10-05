"""SmartThings API integration for device management."""
import asyncio
from typing import List
import aiohttp
import pysmartthings
from decouple import config

# Load SmartThings Personal Access Token
PAT = config('smart_things_pat')

async def list_devices() -> List:
    """
    Retrieve and display all SmartThings devices.

    Returns:
        List of SmartThings device objects
    """
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, PAT)
        devices = await api.devices()

        for i, device in enumerate(devices):
            print(f"Device {i + 1}:")
            print(f"  Name: {device.name}")
            print(f"  ID: {device.device_id}")
            print(f"  Capabilities: {device.capabilities}")
            print('-------------------------')

        return devices

async def main() -> None:
    """Main async function to list SmartThings devices."""
    await list_devices()

if __name__ == "__main__":
    asyncio.run(main())
