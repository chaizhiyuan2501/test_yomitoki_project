import csv
from yomitoku import DocumentAnalyzer
from yomitoku.data.functions import load_image

# 加载图像文件（返回的是一个图像列表，这里取第一张）
# 注意：路径最好用 "/" 或 r"..." 避免转义错误
image = load_image("03_csv_test/images/img1.jpg")[0]

# 初始化 OCR 文档分析器
# 默认使用 CPU，如果你的电脑支持 CUDA/GPU，可以设置 device="cuda"
analyzer = DocumentAnalyzer()

# 执行 OCR 分析，返回结构化结果 + 可视化图像（我们这里只用 result）
result, _, _ = analyzer(image)

# 打开 CSV 文件用于写入，encoding="utf-8" 可正确保存日文字符
with open("03_csv_test/output/result.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)

    # 写入 CSV 表头（列名）
    writer.writerow(["text", "type", "x1", "y1", "x2", "y2"])

    # 写入段落识别结果（正文、标题等）
    for para in result.paragraphs:
        text = para.contents.replace("\n", " ")  # 去除换行，避免 CSV 被分割
        x1, y1, x2, y2 = para.box  # 提取段落的边界框坐标
        writer.writerow([text, "paragraph", x1, y1, x2, y2])

    # 写入表格单元格内容（包括日付、金額等字段）
    for table in result.tables:
        for cell in table.cells:
            text = cell.contents.replace("\n", " ")
            x1, y1, x2, y2 = cell.box
            writer.writerow([text, "table-cell", x1, y1, x2, y2])

    # 写入图像块（如插图、图标）的位置标记
    for fig in result.figures:
        x1, y1, x2, y2 = fig.box
        writer.writerow(["[図表]", "figure", x1, y1, x2, y2])
