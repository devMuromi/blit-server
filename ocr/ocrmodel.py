# # ocr
# import os
# from django.conf import settings
# import cv2
# from PIL import Image, ImageFont, ImageDraw
# import numpy as np

# # easyocr
# from easyocr import Reader

# # azure_vision
# import requests
# import urllib.parse

# # tesseract
# import pytesseract

# from receipt.models import Receipt


# def get_receipt_image(receipt_id):
#     """
#     Get receipt object and image matrix by receipt_id
#     """
#     receipt = Receipt.objects.get(id=receipt_id)
#     image_path = os.path.join(settings.MEDIA_ROOT, str(receipt.image))
#     image = cv2.imread(image_path)
#     return receipt, image


# def create_image_file(receipt, image, ocr_type: str):
#     basename, ext = os.path.splitext(receipt.image.name)
#     new_filename = f"{basename}_{ocr_type}{ext}"
#     new_file_path = os.path.join(settings.MEDIA_ROOT, new_filename)
#     cv2.imwrite(new_file_path, image)


# def modify_image(image, results):
#     fontpath = settings.MEDIA_ROOT + "/fonts/NanumGothicBold.ttf"
#     font = ImageFont.truetype(fontpath, 30)

#     for bbox, text, prob in results:
#         # display the OCR'd text and associated probability
#         # print("[INFO] {:.4f}: {}".format(prob, text))
#         # unpack the bounding box
#         (tl, tr, br, bl) = bbox
#         tl = (int(tl[0]), int(tl[1]))
#         tr = (int(tr[0]), int(tr[1]))
#         br = (int(br[0]), int(br[1]))
#         bl = (int(bl[0]), int(bl[1]))

#         cv2.rectangle(image, tl, br, (0, 255, 0), 2)
#         # pil로 텍스트 출력
#         pil_image = Image.fromarray(image)
#         draw = ImageDraw.Draw(pil_image)
#         draw.text((tl[0], tl[1]), text, (0, 255, 0), font=font)
#         image = np.array(pil_image)

#     return image


# def reg_number(results: list) -> None:
#     for result in results:
#         """
#         remove comma and space from text
#         if 0 is regonized as o or O, change it to 0
#         """
#         result[1] = result[1].replace(" ", "").replace(",", "")

#         chars = list(result[1])
#         if chars[0].isdigit():
#             for i in range(len(chars)):
#                 if chars[i] == "o" or chars[i] == "O":
#                     chars[i] = "0"
#             result[1] = "".join(chars)


# def found_head(results: list):
#     """
#     상품명, 단가, 수량, 금액 표기를 찾아 반환
#     """
#     # 나중에 편집거리 알고리즘 사용해서 인식 애매한것도 찾으면 좋을듯
#     ret = [None, None, None, None]
#     for i in range(len(results)):
#         result = results[i]
#         if result[1] == "상품명" or result[1] == "메뉴":
#             ret[0] = i
#         elif result[1] == "단가":
#             ret[1] = i
#         elif result[1] == "수량":
#             ret[2] = i
#         elif result[1] == "금액":
#             ret[3] = i

#     return ret


# def filter_upperhead(results: list) -> None:
#     heads = found_head(results)
#     highest_y = 0
#     for i in heads:
#         if i != None and results[i][0][0][1] > highest_y:
#             highest_y = results[i][0][0][1]

#     to_remove = [result for result in results if result[0][2][1] < highest_y]
#     for result in to_remove:
#         results.remove(result)


# def easyocr(receipt_id):
#     receipt, image = get_receipt_image(receipt_id)

#     # perform ocr
#     languages = ["ko", "en"]
#     reader = Reader(languages, gpu=False)
#     results = reader.readtext(image)
#     # results: list of result
#     # result format: ([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], text, prob)
#     for i in range(len(results)):
#         results[i] = list(results[i])
#     reg_number(results)
#     filter_upperhead(results)
#     print(results)

#     # add ocr text to receipt image
#     image = modify_image(image, results)
#     # create new image file
#     create_image_file(receipt, image, "easyocr")

#     return results


# def tesseract_ocr(receipt_id):
#     receipt, image = get_receipt_image(receipt_id)

#     # perform OCR using Tesseract
#     ocr_text = pytesseract.image_to_string(image, lang="kor")

#     # loop over the OCR results and print the text
#     print(f"OCR Text:\n{ocr_text}")

#     # draw bounding boxes around the text using OpenCV
#     h, w, _ = image.shape
#     boxes = pytesseract.image_to_boxes(image, lang="eng+kor")
#     for b in boxes.splitlines():
#         b = b.split(" ")
#         x, y, x2, y2 = int(b[1]), h - int(b[2]), int(b[3]), h - int(b[4])
#         cv2.rectangle(image, (x, y), (x2, y2), (0, 255, 0), 2)

#     # create ocr'd image file
#     create_image_file(receipt, image, "tesseract")

#     return ocr_text


# def azure_vision(receipt_id):
#     receipt, image = get_receipt_image(receipt_id)
#     # set the API endpoint and key
#     endpoint = "https://<region>.api.cognitive.microsoft.com/"
#     api_key = "<api_key>"

#     # set the OCR language and URL encoding parameters
#     params = urllib.parse.urlencode(
#         {
#             "language": "ko",
#             "detectOrientation": "true",
#         }
#     )

#     # set the API headers and data
#     headers = {
#         "Content-Type": "application/octet-stream",
#         "Ocp-Apim-Subscription-Key": api_key,
#     }
#     data = open(image_path, "rb").read()

#     # send the API request and get the response
#     response = requests.post(
#         endpoint + "vision/v3.2/ocr?" + params, headers=headers, data=data
#     )
#     response.raise_for_status()

#     # extract the OCR results from the response
#     result = response.json()
#     regions = result["regions"]
#     ocr_text = ""
#     for region in regions:
#         for line in region["lines"]:
#             for word in line["words"]:
#                 ocr_text += word["text"] + " "

#                 # extract the word bounding box coordinates
#                 bbox = word["boundingBox"]
#                 bbox = [int(b) for b in bbox.split(",")]

#                 # draw a green box around the word on the image
#                 cv2.rectangle(
#                     image,
#                     (bbox[0], bbox[1]),
#                     (bbox[0] + bbox[2], bbox[1] + bbox[3]),
#                     (0, 255, 0),
#                     2,
#                 )

#     # update the Receipt instance with the OCR results
#     receipt.ocr_text = ocr_text.strip()
#     receipt.save()

#     # create a new filename for the OCR'd image
#     basename, ext = os.path.splitext(receipt.image.name)
#     new_filename = f"{basename}_azureocr{ext}"
#     new_file_path = os.path.join(settings.MEDIA_ROOT, new_filename)

#     # save the OCR'd image to disk
#     cv2.imwrite(new_file_path, image)

#     return ocr_text
