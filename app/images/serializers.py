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

    def create(self, validated_data):
        """Create a image."""
        user = self.context['request'].user
        print(user)

        image = Image.objects.create(user=user, **validated_data)
        return image

class ImagePremiumUserSerializer(serializers.ModelSerializer):
    """Image model serializer for Premium user"""
    class Meta:
        model = Image
        fields = ('title', 'image_1', 'image_2', 'image')
        read_only_fields = ['image_2', 'image']

    def create(self, validated_data):
        """Create a image."""
        user = self.context['request'].user

        image = Image.objects.create(user=user, **validated_data)
        return image

class ImageEnterpriseUserSerializer(serializers.ModelSerializer):
    pass