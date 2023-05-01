from django.http import HttpResponse
from receipt.models import Receipt

from . import ocrmodel


def ocr(request, pk):
    # ocr_text = easyocr(pk)
    # ocr_text = azure_vision(pk)
    ocr_text = ocrmodel.easyocr(pk)

    return HttpResponse("haha", content_type="text/html")
