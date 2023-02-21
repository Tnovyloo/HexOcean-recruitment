#TODO CREATE VIEWS WITH 'GET_QUERYSET' - FILTERED BY USER AND SERIALIZER CLASS

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Image
from images import serializers


class ImageViewSet(mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """View set for Image model."""
    queryset = Image.objects.all()
    serializer_class = serializers.ImageBasicUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Getting user membership and assign right serializer."""
        user = self.request.user
        print(self.request.user)
        print(self.request.user.membership)
        if user.membership == "BASIC":
            return serializers.ImageBasicUserSerializer
        if user.membership == "PREMIUM":
            return serializers.ImagePremiumUserSerializer

    def get_queryset(self):
        """Filtering queryset by user objects."""
        return self.queryset.filter(user=self.request.user).order_by('-id')