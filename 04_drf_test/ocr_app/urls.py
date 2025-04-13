from django.urls import path
from .views import OCRUploadView

urlpatterns = [
    # 路由: POST /api/ocr/upload/ 调用 OCRUploadView
    path('upload/', OCRUploadView.as_view(), name='ocr-upload'),
]