from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from image.models import Image
from image.serializers import ImageSerializer

@api_view(['GET', 'POST'])
def image_list(request):
    """
    List all images, or create a new image.
    """
    if request.method == 'GET':
        image = Image.objects.all()
        serializer = ImageSerializer(image, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def image_detail(request, pk):
    """
    Retrieve, update or delete an image.
    """
    try:
        image = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        image.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)