from django.http import JsonResponse
from receipt.models import Receipt

import requests
import json
import base64
import os
from django.conf import settings

URL = settings.CLOVA_API_URL
SECRET_KEY = settings.CLOVA_API_KEY


def ocr(request, pk):
    receipt = Receipt.objects.get(id=pk)
    if receipt.data == None:
        image_path = os.path.join(settings.MEDIA_ROOT, str(receipt.image))
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        raw_data, extracted_data = clova_ocr(encoded_string)

        receipt.raw_data = raw_data
        receipt.data = extracted_data
        receipt.save()

    # print(receipt.data)
    return JsonResponse(receipt.data)


def clova_ocr(string_encoded_receipt_image: str) -> tuple[dict, dict]:
    def extract_data(data: dict) -> dict:
        """
        Extract data from ocr result
        return format: {
            "success": "true",
            "store": {
                "name": "name",
                "address": "address",
            },
            "date": {
                "year": "year",
                "month": "month",
                "day": "day",
                "hour": "hour",
                "minute": "minute",
            },
            "items": [
                {
                    "name": "name",
                    "unitPrice": "unitPrice",
                    "count": "count",
                    "price": "price",
                }
            ],
            "totalPrice": "total",
        }
        """

        extracted_data = {
            "success": "true" if data["images"][0]["inferResult"] == "SUCCESS" else "false",
        }
        if extracted_data["success"] == "true":
            data = data["images"][0]["receipt"]["result"]
            extracted_data["date"] = dict()
            extracted_data["items"] = list()
            extracted_data["store"] = dict()
            try:
                extracted_data["date"]["year"] = data["paymentInfo"]["date"]["formatted"]["year"]
                extracted_data["date"]["month"] = data["paymentInfo"]["date"]["formatted"]["month"]
                extracted_data["date"]["day"] = data["paymentInfo"]["date"]["formatted"]["day"]
            except:
                pass
            try:
                extracted_data["date"]["hour"] = data["paymentInfo"]["time"]["formatted"]["hour"]
                extracted_data["date"]["minute"] = data["paymentInfo"]["time"]["formatted"]["minute"]
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
                            "unitPrice": item["price"]["unitPrice"]["formatted"]["value"]
                            if item["price"]["unitPrice"]["formatted"]["value"]
                            else "null",
                            "count": item["count"]["formatted"]["value"] if item["count"]["formatted"]["value"] else "null",
                            "price": item["price"]["price"]["formatted"]["value"]
                            if item["price"]["price"]["formatted"]["value"]
                            else "null",
                        }
                    )
            except:
                pass
            try:
                extracted_data["totalPrice"] = data["result"]["totalPrice"]["formatted"]["value"]
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
