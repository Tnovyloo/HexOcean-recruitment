"""Models for app"""

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from PIL import Image as Img
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

import os.path
import uuid

def image_file_path(instance, filename):
    """Generate file path for new Image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'images', 'original', filename)

def image_file_path_200(instance, filename):
    """Generate file path for new Image 200"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'images', '200', filename)

def image_file_path_400(instance, filename):
    """Generate file path for new Image 400"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'images', '400', filename)


class UserManager(BaseUserManager):
    """Manager for the users."""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email=email,
                                password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Model for the user in the system"""
    MEMBERSHIP = (
        ('BASIC', 'Basic'),
        ('PREMIUM', 'Premium'),
        ('ENTERPRISE', 'Enterprise')
    )

    # NOTES.
    # TODO Create a membership model with specified thumbnail
    # output size. Change Image.image_200 field to image_2 field
    # and also Image.image_400 to image_2. Change this fields in serializer
    # - Might create "CUSTOM" choice in MEMBERSHIP (?)

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    membership = models.CharField(max_length=25, choices=MEMBERSHIP, default='BASIC')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.email}"


class Image(models.Model):
    """Image Model"""

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_file_path)
    image_200 = models.ImageField(upload_to=image_file_path_200, blank=True)
    image_400 = models.ImageField(upload_to=image_file_path_400, blank=True)
    created = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_200 = Img.open(self.image.path)
        img_400 = Img.open(self.image.path)

        output_size_200 = (200, 200)
        output_size_400 = (400, 400)
        img_200.thumbnail(output_size_200)
        img_400.thumbnail(output_size_400)
        img_200.save(self.image_200.path)
        img_400.save(self.image_400.path)
