from easyocr import Reader
from django.core.files.storage import default_storage
from receipt.models import Receipt
from django.conf import settings
import os
from django.http import HttpResponse
import cv2
import urllib.parse
import requests
import pytesseract


def ocr(request, pk):
    # ocr_text = easyocr(pk)
    # ocr_text2 = azure_vision(pk)
    ocr_text3 = tesseract_ocr(pk)

    return HttpResponse(ocr_text3, content_type="text/html")


def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def easyocr(receipt_id):
    # get file with receipt_id
    receipt = Receipt.objects.get(id=receipt_id)
    image_path = os.path.join(settings.MEDIA_ROOT, str(receipt.image))

    # read the image file using OpenCV
    image = cv2.imread(image_path)

    # set the languages to use for OCR
    languages = ["ko", "en"]  # modify as needed

    # perform OCR using EasyOCR
    reader = Reader(languages, gpu=False)
    results = reader.readtext(image)

    # loop over the OCR results and print the text and confidence score
    for bbox, text, score in results:
        print(f"Text: {text}, Confidence score: {score}")
        # unpack the bounding box
        tl = (int(bbox[0][0]), int(bbox[0][1]))
        tr = (int(bbox[1][0]), int(bbox[1][1]))
        br = (int(bbox[2][0]), int(bbox[2][1]))
        bl = (int(bbox[3][0]), int(bbox[3][1]))
        # draw a green box around the text
        cv2.rectangle(image, tl, br, (0, 255, 0), 2)
        # cleanup the text and draw it on the image
        text = cleanup_text(text)
        cv2.putText(
            image,
            text,
            (tl[0], tl[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

    # update the Receipt instance with the OCR results
    receipt.ocr_text = " ".join([text for bbox, text, score in results])
    receipt.save()

    # create a new filename for the OCR'd image
    basename, ext = os.path.splitext(receipt.image.name)
    new_filename = f"{basename}_easyocr{ext}"
    new_file_path = os.path.join(settings.MEDIA_ROOT, new_filename)

    # save the OCR'd image to disk
    cv2.imwrite(new_file_path, image)

    # update the Receipt instance with the path to the OCR'd image file
    # receipt.ocr_image.name = new_filename
    # receipt.save()

    return receipt.ocr_text


def azure_vision(receipt_id):
    # get file with receipt_id
    receipt = Receipt.objects.get(id=receipt_id)
    image_path = os.path.join(settings.MEDIA_ROOT, str(receipt.image))

    # read the image file using OpenCV
    image = cv2.imread(image_path)

    # set the API endpoint and key
    # endpoint = "https://<region>.api.cognitive.microsoft.com/"
    # api_key = "<api_key>"

    # set the OCR language and URL encoding parameters
    language = "ko"
    params = urllib.parse.urlencode(
        {
            "language": language,
            "detectOrientation": "true",
        }
    )

    # set the API headers and data
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": api_key,
    }
    data = open(image_path, "rb").read()

    # send the API request and get the response
    response = requests.post(
        endpoint + "vision/v3.2/ocr?" + params, headers=headers, data=data
    )
    response.raise_for_status()

    # extract the OCR results from the response
    result = response.json()
    regions = result["regions"]
    ocr_text = ""
    for region in regions:
        for line in region["lines"]:
            for word in line["words"]:
                ocr_text += word["text"] + " "

                # extract the word bounding box coordinates
                bbox = word["boundingBox"]
                bbox = [int(b) for b in bbox.split(",")]

                # draw a green box around the word on the image
                cv2.rectangle(
                    image,
                    (bbox[0], bbox[1]),
                    (bbox[0] + bbox[2], bbox[1] + bbox[3]),
                    (0, 255, 0),
                    2,
                )

    # update the Receipt instance with the OCR results
    receipt.ocr_text = ocr_text.strip()
    receipt.save()

    # create a new filename for the OCR'd image
    basename, ext = os.path.splitext(receipt.image.name)
    new_filename = f"{basename}_azureocr{ext}"
    new_file_path = os.path.join(settings.MEDIA_ROOT, new_filename)

    # save the OCR'd image to disk
    cv2.imwrite(new_file_path, image)

    return ocr_text


def tesseract_ocr(receipt_id):
    # get file with receipt_id
    receipt = Receipt.objects.get(id=receipt_id)
    image_path = os.path.join(settings.MEDIA_ROOT, str(receipt.image))

    # read the image file using OpenCV
    image = cv2.imread(image_path)

    # perform OCR using Tesseract
    ocr_text = pytesseract.image_to_string(image, lang="eng+kor")

    # loop over the OCR results and print the text
    print(f"OCR Text:\n{ocr_text}")

    # create a new filename for the OCR'd image
    basename, ext = os.path.splitext(receipt.image.name)
    new_filename = f"{basename}_tesseractocr{ext}"
    new_file_path = os.path.join(settings.MEDIA_ROOT, new_filename)

    # draw bounding boxes around the text using OpenCV
    h, w, _ = image.shape
    boxes = pytesseract.image_to_boxes(image, lang="eng+kor")
    for b in boxes.splitlines():
        b = b.split(" ")
        x, y, x2, y2 = int(b[1]), h - int(b[2]), int(b[3]), h - int(b[4])
        cv2.rectangle(image, (x, y), (x2, y2), (0, 255, 0), 2)

    # save the OCR'd image to disk
    cv2.imwrite(new_file_path, image)

    return ocr_text
