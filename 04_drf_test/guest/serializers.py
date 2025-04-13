from rest_framework import serializers

class ScheduleUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, value):
        # 可加尺寸限制、格式限制等校验逻辑
        return value