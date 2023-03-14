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
        serializer = ImageSerializer(image, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def image_detail(request, pk):
    """
    Retrieve, update or delete an image.
    """
    try:
        image = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ImageSerializer(image)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ImageSerializer(image, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        image.delete()
        return HttpResponse(status=204)