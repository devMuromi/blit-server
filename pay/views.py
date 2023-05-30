from django.http import HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
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
