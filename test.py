import cv2
from yomitoku import DocumentAnalyzer
from yomitoku.data.functions import load_image

PATH_IMAGE = "image\image1.png"

doc_analyzer = DocumentAnalyzer(visualize=True, device="cuda")

image = load_image(PATH_IMAGE)

for i, img in enumerate(image):
    results, ocr_ivs, layout_vis = doc_analyzer(img)
    results.to_html(f"output_{i}.html", img=img)
    cv2.imwrite(f"output_ocr_{i}.jpg", ocr_ivs)
    cv2.imwrite(f"output_layout_{i}.jpg", layout_vis)
