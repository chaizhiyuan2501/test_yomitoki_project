import csv
from yomitoku import DocumentAnalyzer
from yomitoku.data.functions import load_image

image = load_image("03_csv_test\images\img1.jpg")[0]

# 初始化分析器
analyzer = DocumentAnalyzer()
result, _, _ = analyzer(image)

# 直接访问 result.paragraphs / result.tables / result.figures 等属性
with open("03_csv_test\output/result.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "type", "x1", "y1", "x2", "y2"])

    # 段落
    for para in result.paragraphs:
        text = para.contents.replace("\n", " ")
        x1, y1, x2, y2 = para.box
        writer.writerow([text, "paragraph", x1, y1, x2, y2])

    # 表格
    for table in result.tables:
        for cell in table.cells:
            text = cell.contents.replace("\n", " ")
            x1, y1, x2, y2 = cell.box
            writer.writerow([text, "table-cell", x1, y1, x2, y2])

    # 图像块（如果有）
    for fig in result.figures:
        x1, y1, x2, y2 = fig.box
        writer.writerow(["[図表]", "figure", x1, y1, x2, y2])
