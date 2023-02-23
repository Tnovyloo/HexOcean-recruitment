"""
Serializers for Images APIs
"""

from rest_framework import serializers
from core.models import Image


class ImageBasicUserSerializer(serializers.ModelSerializer):
    """Image model serializer for Basic user"""
    class Meta:
        model = Image
        fields = ('title', 'image_1')

class ImagePremiumUserSerializer(serializers.ModelSerializer):
    """Image model serializer for Premium user"""
    class Meta:
        model = Image
        fields = ('title', 'image_1', 'image_2', 'image')