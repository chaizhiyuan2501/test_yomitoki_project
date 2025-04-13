from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from yomitoku import DocumentAnalyzer
from yomitoku.data.functions import load_image
from .serializers import OCRImageSerializer
from PIL import Image
import numpy as np
import cv2
import os


class OCRUploadView(APIView):
    # 支持图片文件的 multipart 解析
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        # 验证上传数据（是否有 image 文件）
        serializer = OCRImageSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data["image"]  # 获取图片文件
            temp_path = f"temp_{image_file.name}"  # 临时文件名
            with open(temp_path, "wb") as f:  # 保存文件到本地
                for chunk in image_file.chunks():
                    f.write(chunk)

            # 初始化 Yomitoku 文档分析器
            analyzer = DocumentAnalyzer(configs={})
            # 加载图像 + 转 RGB + 转 ndarray + 转 BGR
            image = Image.open(temp_path).convert("RGB")
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            result, _, _ = analyzer(image)  # 执行 OCR 分析

            os.remove(temp_path)  # 删除临时文件

            return Response(result.model_dump(), status=200)  # 返回 JSON 结果
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response({"message": "请使用 POST 上传图片文件进行 OCR 识别。"})
