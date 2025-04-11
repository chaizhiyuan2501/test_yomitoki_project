import os
import cv2
from glob import glob
from yomitoku import DocumentAnalyzer
from yomitoku.data.functions import load_image

# 设置输入输出路径
INPUT_DIR = ".\images"
OUTPUT_DIR = ".\output"

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 初始化分析器
doc_analyzer = DocumentAnalyzer(visualize=True, device="cuda")  # 若无GPU可设为 "cpu"

# 获取所有图片文件
image_files = glob(os.path.join(INPUT_DIR, "*.[pjPJ]*[npNP]*[gG]"))  # 匹配 png/jpg/jpeg 大小写

for idx, path in enumerate(image_files):
    images = load_image(path)
    print(f"🔍 处理图像: {path}")

    for i, img in enumerate(images):
        results, ocr_ivs, layout_vis = doc_analyzer(img)

        base_name = os.path.splitext(os.path.basename(path))[0]
        suffix = f"{idx}_{i}" if len(images) > 1 else f"{idx}"

        html_path = os.path.join(OUTPUT_DIR, f"{base_name}_{suffix}.html")
        ocr_img_path = os.path.join(OUTPUT_DIR, f"{base_name}_{suffix}_ocr.jpg")
        layout_img_path = os.path.join(OUTPUT_DIR, f"{base_name}_{suffix}_layout.jpg")

        results.to_html(html_path, img=img)
        cv2.imwrite(ocr_img_path, ocr_ivs)
        cv2.imwrite(layout_img_path, layout_vis)

print("✅ 批量 OCR 完成！")
