import os
import aiohttp
import asyncio
from PIL import Image
from io import BytesIO
import sys

class Fetcher:
    def __init__(self, api, terms, **kwargs):
        self.api = api
        self.terms = terms
        self.key = kwargs.get("key")
        self.engine_id = kwargs.get("engine_id")

    async def fetch(self, count_per_class=100):
        fetchers = {
            "hugging_face": hugging_face_fetch,
            "google": google_fetch,
            "bing": bing_fetch
            # Add other API fetch functions here if needed
        }

        fetcher = fetchers.get(self.api)
        
        if fetcher is None:
            raise ValueError(f"API '{self.api}' not supported")

        if self.api == "hugging_face":
            self.urls = await fetcher(self.terms, count_per_class)
        
        elif self.api == "google":
            if not self.key or not self.engine_id:
                raise ValueError("API key and engine ID must be provided for Google search")        
            self.urls = await fetcher(self.key, self.engine_id, self.terms, count_per_class)
        
        elif self.api == "bing":
            if not self.key:
                raise ValueError("API key must be provided for Bing search")
            self.urls = await fetcher(self.key, self.terms, count_per_class)
        
        return self.urls

    async def download(self, dir):
        pass
