#TODO CREATE VIEWS WITH 'GET_QUERYSET' - FILTERED BY USER AND SERIALIZER CLASS

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from core.models import Image
from .serializers import (ImageBasicUserSerializer,
                        ImagePremiumUserSerializer,
                        ImageEnterpriseUserSerializer,
)



class ImageViewSet(mixins.ListModelMixin,
                        # mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """View set for Image model."""
    queryset = Image.objects.all()
    serializer_class = ImageBasicUserSerializer
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # @swagger_auto_schema(query_serializer=ImagePremiumUserSerializer(), responses={200: ImagePremiumUserSerializer()},)
    def get_serializer_class(self):
        """Getting user membership and assign right serializer."""
        user = self.request.user

        # FOR OLD ONE IN MODELS CHOICES
        # if user.membership == "BASIC":
        #     return ImageBasicUserSerializer
        # if user.membership == "PREMIUM":
        #     return ImagePremiumUserSerializer

        # FOR NEW ONE WHEN TIER IS A MODEL
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