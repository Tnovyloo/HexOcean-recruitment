"""
Serializers for Images APIs
"""

from rest_framework import serializers
from core.models import Image, URLExpiration


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
        read_only_fields = ['image', 'image_2']

    def create(self, validated_data):
        """Create a image."""
        user = self.context['request'].user

        image = Image.objects.create(user=user, **validated_data)
        return image


class URLExpirationSerializer(serializers.ModelSerializer):
    """Image URL serializer"""
    class Meta:
        model = URLExpiration
        fields = ('image', 'time')
        read_only_fields = ['url']


class ImageEnterpriseUserSerializer(serializers.ModelSerializer):
    """Image model serializer for Enterprise user"""
    # urls = URLExpirationSerializer()

    class Meta:
        model = Image
        fields = ('image_id', 'title', 'image_1', 'image_2', 'image')
        read_only_fields = ['image_id', 'image', 'image_2']