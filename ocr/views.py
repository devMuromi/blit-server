from django.http import JsonResponse, Http404
from receipt.models import Receipt
from django.core.exceptions import PermissionDenied

from rest_framework.decorators import api_view, permission_classes
from receipt import permissions as custom_permissions
from rest_framework import permissions

import requests
import json
import base64
import os
from django.conf import settings

URL = settings.CLOVA_API_URL
SECRET_KEY = settings.CLOVA_API_KEY


@api_view(["GET"])
def ocr(request, pk):
    try:
        receipt = Receipt.objects.get(id=pk)
        if request.user != receipt.uploaded_by:
            raise PermissionDenied

        if receipt.data == None:
            image_path = os.path.join(settings.MEDIA_ROOT, str(receipt.image))
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

            raw_data, extracted_data = clova_ocr(encoded_string)

            receipt.raw_data = raw_data
            receipt.data = extracted_data
            receipt.save()

        return JsonResponse(receipt.data)
    except Receipt.DoesNotExist:
        raise Http404


def clova_ocr(string_encoded_receipt_image: str) -> tuple[dict, dict]:
    def extract_data(data: dict) -> dict:
        """
        Extract data from ocr result
        return format: {
            "success": bool_IS_SUCCESS,
            "store": {
                "name": "str_NAME",
                "address": "str_ADDRESS",
            },
            "date": {
                "year": int_YEAR,
                "month": int_MONTH,
                "day": int_DAY,
                "hour": int_HOUR,
                "minute": int_MINUTE,
            },
            "items": [
                {
                    "name": "str_NAME",
                    "unitPrice": int_UNIT_PRICE,
                    "count": int_COUNT,
                    "price": int_PRICE,
                },
            ],
            "totalPrice": int_TOTAL_PRICE,
        }
        """

        extracted_data = {
            "success": True if data["images"][0]["inferResult"] == "SUCCESS" else False,
        }
        if extracted_data["success"] == True:
            data = data["images"][0]["receipt"]["result"]
            extracted_data["date"] = dict()
            extracted_data["items"] = list()
            extracted_data["store"] = dict()
            try:
                extracted_data["date"]["year"] = int(data["paymentInfo"]["date"]["formatted"]["year"])
                extracted_data["date"]["month"] = int(data["paymentInfo"]["date"]["formatted"]["month"])
                extracted_data["date"]["day"] = int(data["paymentInfo"]["date"]["formatted"]["day"])
            except:
                pass
            try:
                extracted_data["date"]["hour"] = int(data["paymentInfo"]["time"]["formatted"]["hour"])
                extracted_data["date"]["minute"] = int(data["paymentInfo"]["time"]["formatted"]["minute"])
            except:
                pass
            try:
                extracted_data["store"]["name"] = data["storeInfo"]["name"]["formatted"]["value"]
            except:
                pass
            try:
                extracted_data["store"]["address"] = data["storeInfo"]["addresses"][0]["formatted"]["value"]
            except:
                pass
            try:
                for item in data["subResults"][0]["items"]:
                    extracted_data["items"].append(
                        {
                            "name": item["name"]["formatted"]["value"] if item["name"]["formatted"]["value"] else "null",
                            "unitPrice": int(item["price"]["unitPrice"]["formatted"]["value"])
                            if item["price"]["unitPrice"]["formatted"]["value"]
                            else None,
                            "count": int(item["count"]["formatted"]["value"]) if item["count"]["formatted"]["value"] else None,
                            "price": int(item["price"]["price"]["formatted"]["value"])
                            if item["price"]["price"]["formatted"]["value"]
                            else None,
                        }
                    )
            except:
                pass
            try:
                extracted_data["totalPrice"] = int(data["result"]["totalPrice"]["formatted"]["value"])
            except:
                pass

        return extracted_data

    data = {
        "version": "V2",
        "requestId": "example",
        "resultType": "string",
        "timestamp": 0,
        "images": [{"format": "jpg", "data": string_encoded_receipt_image, "name": "demo"}],
    }
    headers = {"X-OCR-SECRET": SECRET_KEY, "Content-Type": "application/json"}
    response = requests.post(URL, data=json.dumps(data), headers=headers)
    raw_data = json.loads(response.text)
    print("clova ocr 완료", raw_data)
    extracted_data = extract_data(raw_data)

    return raw_data, extracted_data
