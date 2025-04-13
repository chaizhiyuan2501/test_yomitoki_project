import os
import cv2
from yomitoku import DocumentAnalyzer
from yomitoku.data.functions import load_image

PATH_IMAGE = ".\images\image1.png"
OUTPUT_DIR = ".\output"

doc_analyzer = DocumentAnalyzer(visualize=True, device="cuda")

image = load_image(PATH_IMAGE)

for i, img in enumerate(image):
    results, ocr_ivs, layout_vis = doc_analyzer(img)
    results.to_html(f"{OUTPUT_DIR}/output_{i}.html", img=img)
    cv2.imwrite(f"{OUTPUT_DIR}/output_ocr_{i}.jpg", ocr_ivs)
    cv2.imwrite(f"{OUTPUT_DIR}/output_layout_{i}.jpg", layout_vis)
