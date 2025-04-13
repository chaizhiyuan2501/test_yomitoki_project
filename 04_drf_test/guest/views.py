from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import ScheduleUploadSerializer
from utils.ocr_schedule_parser import analyze_schedule_image, save_guest_schedule

import os

class ScheduleUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = ScheduleUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            temp_path = f"temp_{image_file.name}"
            with open(temp_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
            try:
                result = analyze_schedule_image(temp_path)
                count = save_guest_schedule(result)
            except Exception as e:
                os.remove(temp_path)
                return Response({"error": str(e)}, status=500)
            os.remove(temp_path)
            return Response({"message": f"{count}件の訪問スケジュールを保存しました。", "guest": result['name']}, status=200)
        return Response(serializer.errors, status=400)
