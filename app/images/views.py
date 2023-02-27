from rest_framework import viewsets, mixins, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from core.models import Image, URLExpiration
from .serializers import (ImageBasicUserSerializer,
                        ImagePremiumUserSerializer,
                        ImageEnterpriseUserSerializer,
                        URLExpirationSerializer
)

class BaseViewSet(mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    """Base ViewSet."""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ImageViewSet(BaseViewSet):
    """View set for Image model."""
    queryset = Image.objects.all()
    serializer_class = ImageBasicUserSerializer

    def get_serializer_class(self):
        """Getting user membership and assign right serializer."""
        user = self.request.user

        if user.membership.tier_name == "BASIC":
            return ImageBasicUserSerializer
        if user.membership.tier_name == "PREMIUM":
            return ImagePremiumUserSerializer
        if user.membership.tier_name != "BASIC" and \
            user.membership.tier_name != "PREMIUM":
            return ImageEnterpriseUserSerializer

    def get_queryset(self):
        """Filtering queryset by user objects."""
        return self.queryset.filter(user=self.request.user).order_by('-id')


class CreateURLViewSet(BaseViewSet):
    """View for creating URL with expiration"""
    queryset = URLExpiration.objects.all()
    serializer_class = URLExpirationSerializer

    def get_queryset(self):
        """Filtering queryset by user Image objects"""
        return self.queryset.filter(image__user=self.request.user).order_by('-id')
