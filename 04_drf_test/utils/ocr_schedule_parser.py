import re
import os
import numpy as np
import cv2
from PIL import Image
from yomitoku import DocumentAnalyzer
from guest.models import Guest, VisitType, VisitSchedule


VISIT_TYPE_MAPPING = {
    "泊": "泊まり",
    "通い": "通い",
    "休": "休み",
}

def analyze_schedule_image(image_path):
    # 从文件名提取姓名、年份、月份
    filename = os.path.basename(image_path)
    name_match = re.search(r"_(.+?)_", filename)
    date_match = re.search(r"(\d{4})[\u5e74/-]?(\d{1,2})", filename)

    guest_name = name_match.group(1) if name_match else "不明"
    year = date_match.group(1) if date_match else "2025"
    month = f"{int(date_match.group(2)):02d}" if date_match else "04"

    # 加载图片并转换为 OpenCV 格式
    image = Image.open(image_path).convert("RGB")
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 运行 OCR
    analyzer = DocumentAnalyzer(configs={})
    result, _, _ = analyzer(image)

    schedule = []

    print("\n📝 OCR分析されたテーブル数：", len(result.tables))
    for table in result.tables:
        for cell in table.cells:
            content = cell.contents.strip().replace("\n", " ")
            print(f"行: {cell.row} 列: {cell.col} 内容: {content}")
            # 匹配包含日期和来访类型的内容
            if any(x in content for x in VISIT_TYPE_MAPPING.keys()):
                match = re.search(r"(\d{1,2}).*?(泊|通い|休)", content)
                if match:
                    day = int(match.group(1))
                    visit_code = match.group(2)
                    visit_type_name = VISIT_TYPE_MAPPING.get(visit_code)
                    schedule.append({
                        "date": f"{year}-{month}-{day:02d}",
                        "type": visit_type_name
                    })

    return {
        "name": guest_name,
        "year": year,
        "month": month,
        "schedule": schedule
    }

def save_guest_schedule(result):
    name = result['name']
    schedule = result['schedule']

    guest, _ = Guest.objects.get_or_create(name=name)

    created_count = 0
    for item in schedule:
        date = item['date']
        type_name = item['type']
        print(f"📅 保存中: {date} - {type_name}")

        try:
            visit_type = VisitType.objects.get(name=type_name)
        except VisitType.DoesNotExist:
            print(f"⚠️ VisitType 不存在: {type_name}")
            continue
        except Exception as e:
            print("❌ VisitType 取得失败:", e)
            continue

        try:
            _, created = VisitSchedule.objects.update_or_create(
                guest=guest,
                date=date,
                defaults={"visit_type": visit_type}
            )
            if created:
                created_count += 1
        except Exception as e:
            print("❌ VisitSchedule 保存失败:", e)
            continue

    return created_count