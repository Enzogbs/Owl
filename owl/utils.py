import aiohttp
import asyncio
from PIL import Image
from io import BytesIO

async def download_image(session, url, path):
    failed = 0
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            img_data = await response.read()
            img = Image.open(BytesIO(img_data))
            img_format = img.format.lower()
            img.save(path)
            print(f"Downloaded: {path}")
    
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        failed += 1
