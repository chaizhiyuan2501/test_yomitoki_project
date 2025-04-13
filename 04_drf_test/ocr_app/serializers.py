from rest_framework import serializers

class OCRImageSerializer(serializers.Serializer):
    # 图片上传的基本验证器，确保字段是图片类型
    image = serializers.ImageField()
