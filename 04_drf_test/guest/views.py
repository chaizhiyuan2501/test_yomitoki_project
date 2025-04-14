from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ScheduleUploadSerializer
from utils.ocr_utils import ScheduleOCRProcessor
import tempfile

class ScheduleUploadView(APIView):
    """
    画像から訪問スケジュールを抽出し、DBに保存するAPI。
    """

    def post(self, request, *args, **kwargs):
        serializer = ScheduleUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image_file = serializer.validated_data['image']

        # 一時ファイルに保存して処理（PILとOpenCVに対応するため）
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(image_file.read())
            temp_path = temp_file.name

        # OCR解析 & DB保存
        processor = ScheduleOCRProcessor(temp_path)
        result = processor.run()

        return Response({
            "message": f"{result['count']}件の訪問スケジュールを保存しました。",
            "guest": result['guest'],
            "year": result['year'],
            "month": result['month']
        }, status=status.HTTP_200_OK)
