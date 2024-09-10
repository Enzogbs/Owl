import requests

def bing_fetch(key: str, search_term: str, count: str):
	SEARCH_URL = "https://api.bing.microsoft.com/v7.0/images/search"

	headers = {"Ocp-Apim-Subscription-Key" : key}

	params  = {
		"q": search_term, 
		"license": "public", 
		"imageType": "photo",
		"count": count
		}

	try:
		response = requests.get(search_url, headers=headers, params=params)
		response.raise_for_status()
		response_data = response.json()
		image_urls = [img["thumbnailUrl"] for img in response_data["value"][:16]]

	except Exception as e:
		print("Failed to fetch images")

	return image_urls

def google_fetch(key: str, engine_id: str, search_term: str, count: int):	
	SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

	params = {
		"q": search_term,
		"key": key,
		"cx": engine_id,
		"searchType": "image",
		"filter": 1
		}
	
	image_urls = []
	metadata = []
	start = 1

	while len(image_urls) < count:
		params["start"] = start
		
		try:
			response = requests.get(SEARCH_URL, params=params)
			response.raise_for_status()
			response_data = response.json()
			items = response_data["items"]

			if not items:
				break

			image_urls.extend([img["link"] for img in items])
			metadata.extend([img for img in items])

			start += 10

		except Exception as e:
			print("Failed to fetch images")
			continue

	return image_urls, metadata		
	

def hugging_face_fetch(search_term: str, count: int):
    SEARCH_URL = "https://huggingpics-api-server.fly.dev/images/search"

    params = {
        "q": search_term,
        "license": "public",
        "imageType": "photo",
        "count": count
    	}

    try:
    	response = requests.get(SEARCH_URL, params=params)
    	response.raise_for_status()
    	response_data = response.json()
    	image_urls = [img["thumbnailUrl"] for img in response_data["value"]]
    	metadata = [img for img in response_data["value"]]

    except Exception as e:
    	print("Failed to fetch images")

    return image_urls, metadata
