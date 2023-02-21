"""URL mappings for the images app"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from images import views

router = DefaultRouter()
router.register('images', views.ImageViewSet)

app_name = 'images'

urlpatterns = [
    path('', include(router.urls)),
]