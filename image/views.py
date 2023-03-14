from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from image.models import Image
from image.serializers import ImageSerializer

@csrf_exempt
def image_list(request):
    """
    List all images, or create a new image.
    """
    if request.method == 'GET':
        image = Image.objects.all()
        serializer = ImageSerialier(image, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)