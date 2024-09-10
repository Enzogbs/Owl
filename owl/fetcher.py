import os
from PIL import Image
from io import BytesIO
import sys
from .apis import google_fetch, hugging_face_fetch, bing_fetch
from .utils import download_image

class Fetcher:
    def __init__(self, api, terms, **kwargs):
        self.api = api
        self.terms = terms
        self.key = kwargs.get("key")
        self.engine_id = kwargs.get("engine_id")

    def fetch(self, count_per_class=100):
        self.urls_dict = {}
        self.count_per_class = count_per_class

        fetchers = {
            "hugging_face": hugging_face_fetch,
            "google": google_fetch,
            "bing": bing_fetch
            # Add other API fetch functions here if needed
        }

        fetcher = fetchers.get(self.api)

        if fetcher is None:
            raise ValueError(f"API '{self.api}' not supported")

        for term in self.terms:
        	if self.api == "hugging_face":
        		urls = fetcher(term, count_per_class)
        	elif self.api == "google":
        		urls = fetcher(self.key, self.engine_id, term, count_per_class)
        	elif self.api == "bing":
        		urls = fetcher(self.key, term, count_per_class)

        	self.urls_dict[term] = urls
        
        return self.urls_dict

    def download(self, download_dir, organize=True, numeric_classes=True, split=None, resize=None, verbose=False):
	    total_count = 0
	    failed_count = 0
	    
	    if not os.path.exists(download_dir):
	        os.makedirs(download_dir, exist_ok=True)
	    
	    if organize and split:
	        if len(split) != 3 or not all(0 <= p <= 100 for p in split) or sum(split) != 100:
	            raise ValueError("Split must be a tuple of three percentages summing up to 100")
	        
	        split_folders = ["train", "test", "validation"]
	        split_counts = {folder: math.floor(p / 100 * sum(len(urls) for urls in self.urls_dict.values())) for folder, p in zip(split_folders, split)}
	        print(split_counts)

	        for folder in split_folders:
	            os.makedirs(os.path.join(download_dir, folder), exist_ok=True)
	            for term in self.terms:
	                term_ = term
	                if numeric_classes:
	                	term_ = self.terms.index(term)
	                os.makedirs(os.path.join(download_dir, folder, str(term_)), exist_ok=True)
	    
	    if organize:
		    for term in self.urls_dict:
		        term_index = str(self.terms.index(term)) if numeric_classes else term
		        term_images = self.urls_dict[term]
		        num_images = len(term_images)
		        
		        if split:
		            images_remaining = term_images[:]
		            for folder in split_folders:
		                folder_path = os.path.join(download_dir, folder, term_index)
		                os.makedirs(folder_path, exist_ok=True)
		                num_to_download = int(split_counts[folder]//3)
		                images_to_download = images_remaining[:num_to_download]
		                images_remaining = images_remaining[num_to_download:]

		                for idx, url in enumerate(images_to_download):
		                    img_path = os.path.join(folder_path, f"{term}_image_{idx+1}.jpg")
		                    success = download_image(url, img_path, resize=resize, verbose=verbose)
		                    if success:
		                        total_count += 1
		                    else:
		                        failed_count += 1
		                
		        else:
		            term_path = os.path.join(download_dir, term_index)
		            os.makedirs(term_path, exist_ok=True)

		            for idx, url in enumerate(term_images):
		                img_path = os.path.join(term_path, f"{term}_image_{idx+1}.jpg")
		                success = download_image(url, img_path, resize=resize, verbose=verbose)
		                if success:
		                    total_count += 1
		                else:
		                    failed_count += 1
	    else:
	    	for term in self.urls_dict:
	    		term_images = self.urls_dict[term]

	    		for idx, url in enumerate(term_images):
	    			img_path = os.path.join(download_dir, f"{term}_image_{idx+1}.jpg")
	    			success = download_image(url, img_path, resize=resize, verbose=verbose)
	    			if success:
	    				total_count += 1
	    			else:
	    				failed_count += 1 

	    print("Downloads finished")
	    print(f"Total images downloaded: {total_count}")
	    print(f"Images failed to download: {failed_count}")

fetcher = Fetcher(api="hugging_face", terms=["cat", "dog", "monkey"])
urls = fetcher.fetch(30)
fetcher.download(download_dir="C:\\Users\\enzog\\PycharmProjects\\PYTHON\\Owl\\images", organize=True, numeric_classes=True, split=None, resize=(224, 224), verbose=True)
