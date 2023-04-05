from easyocr import Reader
import argparse
import cv2
from PIL import Image, ImageFont, ImageDraw
import numpy as np


# 영수증의 roi 따기
# 그 안에서 품목들의 roi 따기.


def found_row(text: str):
    """
    check if text is a row
    """


# Example usage
input_str = "I have 3 oranges and 4 apples."
output_str = fix_numbers(input_str)
print(output_str)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image to be OCR'd")
ap.add_argument(
    "-l",
    "--langs",
    type=str,
    default="ko,en",
    help="comma separated list of languages to OCR",
)
ap.add_argument(
    "-g", "--gpu", type=int, default=-1, help="whether or not GPU should be used"
)

args = vars(ap.parse_args())

# break the input languages into a comma separated list
langs = args["langs"].split(",")
print("[INFO] OCR'ing with the following languages: {}".format(langs))
# load the input image from disk
image = cv2.imread(args["image"])
# OCR the input image using EasyOCR
print("[INFO] OCR'ing input image...")

reader = Reader(langs, gpu=args["gpu"] > 0)
results = reader.readtext(image)

# 한글 폰트 로드
fontpath = "./media/fonts/NanumGothicBold.ttf"
font = ImageFont.truetype(fontpath, 30)

# loop over the results
# result type: ([[x1,y1] [x2,y2] [x3,y3] [x4,y4]], 'text', 0.9999)
for bbox, text, prob in results:
    # display the OCR'd text and associated probability
    print("[INFO] {:.4f}: {}".format(prob, text))
    # unpack the bounding box
    (tl, tr, br, bl) = bbox
    tl = (int(tl[0]), int(tl[1]))
    tr = (int(tr[0]), int(tr[1]))
    br = (int(br[0]), int(br[1]))
    bl = (int(bl[0]), int(bl[1]))

    cv2.rectangle(image, tl, br, (0, 255, 0), 2)
    text = fix_numbers(text)
    # pil로 텍스트 출력
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)
    draw.text((tl[0], tl[1]), text, (0, 255, 0), font=font)
    image = np.array(pil_image)
# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)
