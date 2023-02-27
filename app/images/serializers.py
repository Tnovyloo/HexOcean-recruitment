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
        fields = ('image', 'time', 'url')
        read_only_fields = ['url']

    def create(self, validated_data):
        user = self.context['request'].user
        if user.membership.is_able_to_create_url:
            url = URLExpiration.objects.create(**validated_data)
            return url
        else:
            return False


class ImageEnterpriseUserSerializer(serializers.ModelSerializer):
    """Image model serializer for Enterprise user"""

    class Meta:
        model = Image
        fields = ('image_id', 'title', 'image_1', 'image_2', 'image')
        read_only_fields = ['image_id', 'image', 'image_2']