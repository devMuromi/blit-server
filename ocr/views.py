import easyocr
from receipt.models import Receipt
from django.conf import settings
import os
from django.http import HttpResponse


def ocr(request, pk):
    file_name = Receipt.objects.get(id=pk).image.name

    reader = easyocr.Reader(["ko", "en"])
    results = reader.readtext(os.path.join(settings.MEDIA_ROOT, file_name))
    print(results)
    html = "<br>".join([result[1] for result in results])
    return HttpResponse(html, content_type="text/html")
