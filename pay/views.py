from django.shortcuts import render
import requests
import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse


def test(request):
    a = get_image_by_name("카페라떼")
    print(a)
    return HttpResponse(a)


def get_image_by_name(menu_name: str) -> str:
    """
    Get menu name and returns image URL using bing image web search API
    """

    subscription_key = settings.AZURE_BING_SEARCH_API_KEY
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    search_term = menu_name

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

    # image_data = requests.get(thumbnail_url)
    # image_data.raise_for_status()
    # image = Image.open(BytesIO(image_data.content))

    # plt.imshow(image)
    # plt.axis("off")
    # plt.show()

    return thumbnail_url
