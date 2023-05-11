import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO


search_url = "https://api.bing.microsoft.com/v7.0/images/search"
search_term = "카페라떼"

headers = {"Ocp-Apim-Subscription-Key": subscription_key}

params = {
    "q": search_term,
    "imageType": "photo",
    "count": 1,
    "cc": "ko",
    "mkt": "ko-KR",
    "setLang": "ko-KR",
    "imageType": "photo",
}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()
thumbnail_url = search_results["value"][0]["thumbnailUrl"]

image_data = requests.get(thumbnail_url)
image_data.raise_for_status()
image = Image.open(BytesIO(image_data.content))

plt.imshow(image)
plt.axis("off")
plt.show()
