import aiohttp
import asyncio


def bing_fetch(key: str, search_term: str, count: str):
    SEARCH_URL = "https://api.bing.microsoft.com/v7.0/images/search"

    headers = {"Ocp-Apim-Subscription-Key" : key}

    params  = {
        "q": search_term, 
        "license": "public", 
        "imageType": "photo",
        "count": count
        }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(SEARCH_URL, params=params) as response:
                response.raise_for_status()
                response_data = await response.json()
                image_urls = [img["thumbnailUrl"] for img in response_data["value"]]
        
        except aiohttp.ClientError as e:
            print(f"HTTP request failed: {e}")
            break
        
        except KeyError as e:
            print(f"Unexpected response format: {e}")
            break

    return image_urls

async def google_fetch(key: str, engine_id: str, search_term: str, count: int):
    SEARCH_URL = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        "q": search_term,
        "key": key,
        "cx": engine_id,
        "searchType": "image",
        "filter": 1
        }
    
    image_urls = []
    start = 1

    async with aiohttp.ClientSession() as session:
        while len(image_urls) < count:
            params['start'] = start
            try:
                async with session.get(SEARCH_URL, params=params) as response:
                    response.raise_for_status()
                    response_data = await response.json()
                    items = response_data["items"]
                    
                    if not items:
                        break

                    image_urls.extend([img["link"] for img in items])
                    
                    start += 10
            
            except aiohttp.ClientError as e:
                print(f"HTTP request failed: {e}")
                break
            
            except KeyError as e:
                print(f"Unexpected response format: {e}")
                break

    return image_urls

async def hugging_face_fetch(search_term: str, count: int):
    SEARCH_URL = "https://huggingpics-api-server.fly.dev/images/search"
    params = {
        "q": search_term,
        "license": "public",
        "imageType": "photo",
        "count": count
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(SEARCH_URL, params=params) as response:
                response.raise_for_status()
                response_data = await response.json()
                image_urls = [img["thumbnailUrl"] for img in response_data["value"]]
        
        except aiohttp.ClientError as e:
            print(f"HTTP request failed: {e}")
            break
        
        except KeyError as e:
            print(f"Unexpected response format: {e}")
            break                
    
    return image_urls
