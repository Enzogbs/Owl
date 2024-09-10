import requests
from PIL import Image
from io import BytesIO

def download_image(url, path, resize, verbose=True):
	try:
		response = requests.get(url)
		response.raise_for_status()
		img_data = response.content
		img = Image.open(BytesIO(img_data))

		if resize is not None:
			img = img.resize(resize)

		img.save(path)
		
		if verbose:
			print(f"Downloaded: {path}")
		return True

	except Exception as e:
		print(f"Failed to download {url}: {e}")
		return False
