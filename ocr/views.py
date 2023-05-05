from django.http import HttpResponse
from receipt.models import Receipt

import requests
import json
import base64
import os
import cv2
from django.conf import settings

# from . import ocrmodel


def ocr(request, pk):
    # ocr_text = easyocr(pk)
    # ocr_text = azure_vision(pk)
    ret = clova_ocr(pk)
    print(ret)

    return HttpResponse(json.dumps(ret), content_type="text/html")


def clova_ocr(receipt_id: int) -> dict:
    def get_receipt_image(receipt_id):
        """
        Get receipt object and image matrix by receipt_id
        """
        receipt = Receipt.objects.get(id=receipt_id)
        image_path = os.path.join(settings.MEDIA_ROOT, str(receipt.image))
        image = cv2.imread(image_path)
        return receipt, image

    def extract_data(data: dict) -> dict:
        """
        Extract data from ocr result
        return format: {
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
                    "unitPrice": "unitPrice:int",
                    "count": "count:int",
                    "price": "price:int",
                }
            ],
            "totalPrice": "total:int",
            "success": "true",
        }
        """
        data = data["images"][0]
        extracted_data = {
            "success": "true" if data["inferResult"] == "SUCCESS" else "false",
            "store": {
                "name": data["receipt"]["result"]["storeInfo"]["name"]["formatted"][
                    "value"
                ],
                "address": data["receipt"]["result"]["storeInfo"]["addresses"][0][
                    "formatted"
                ]["value"],
            },
            "date": {
                "year": data["receipt"]["result"]["paymentInfo"]["date"]["formatted"][
                    "year"
                ],
                "month": data["receipt"]["result"]["paymentInfo"]["date"]["formatted"][
                    "month"
                ],
                "day": data["receipt"]["result"]["paymentInfo"]["date"]["formatted"][
                    "day"
                ],
                "hour": data["receipt"]["result"]["paymentInfo"]["time"]["formatted"][
                    "hour"
                ],
                "minute": data["receipt"]["result"]["paymentInfo"]["time"]["formatted"][
                    "minute"
                ],
                "second": data["receipt"]["result"]["paymentInfo"]["time"]["formatted"][
                    "second"
                ],
            },
            "items": [],
        }
        for item in data["receipt"]["result"]["subResults"][0]["items"]:
            extracted_data["items"].append(
                {
                    "name": item["name"]["formatted"]["value"],
                    "unitPrice": item["price"]["unitPrice"]["formatted"]["value"],
                    "count": item["count"]["formatted"]["value"],
                    "price": item["price"]["price"]["formatted"]["value"],
                }
            )
        return extracted_data

    receipt, image = get_receipt_image(receipt_id)

    image_data = cv2.imencode(".jpg", image)[1].tostring()
    encoded_string = base64.b64encode(image_data).decode("utf-8")

    data = {
        "version": "V2",
        "requestId": "example",
        "resultType": "string",
        "timestamp": 0,
        "images": [{"format": "jpg", "data": encoded_string, "name": "demo"}],
    }
    headers = {"X-OCR-SECRET": SECRET_KEY, "Content-Type": "application/json"}
    response = requests.post(URL, data=json.dumps(data), headers=headers)
    raw_data = json.loads(response.text)
    extracted_data = extract_data(raw_data)
    print(extracted_data)

    return extracted_data
