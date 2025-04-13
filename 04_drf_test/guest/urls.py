from django.urls import path
from .views import ScheduleUploadView

urlpatterns = [
    path("schedule-upload/", ScheduleUploadView.as_view(), name="schedule-upload"),
]  # POST /api/ocr/schedule-ocr/
