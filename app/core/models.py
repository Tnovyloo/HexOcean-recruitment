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

def image_file_path_1(instance, filename):
    """Generate file path for new Image 200"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'images', '1', filename)

def image_file_path_2(instance, filename):
    """Generate file path for new Image 400"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'images', '2', filename)


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


class Membership(models.Model):
    """Membership for """
    tier_name = models.CharField(max_length=255, unique=True)
    image_1_height = models.IntegerField(null=False)
    image_1_width = models.IntegerField(null=False)
    image_2_height = models.IntegerField(null=True)
    image_2_width = models.IntegerField(null=True)

    def __str__(self):
        return self.tier_name

    @classmethod
    def get_default_pk(cls):
        tier, created = cls.objects.get_or_create(
            tier_name="BASIC",
            image_1_height=200,
            image_1_width=200
        )
        return tier.pk


# def get_basic_membership():
#     object = Membership.objects.get_or_create(tier_name="PREMIUM",
#                                      image_1_height=200,
#                                      image_1_width=200,
#                                      image_2_height=400,
#                                      image_2_width=400)
#     object.save()
#     return Membership.objects.get_or_create(tier_name="BASIC",
#                                             image_1_height=200,
#                                             image_1_width=200)[0].id


class User(AbstractBaseUser, PermissionsMixin):
    """Model for the user in the system"""
    # MEMBERSHIP = (
    #     ('BASIC', 'Basic'),
    #     ('PREMIUM', 'Premium'),
    #     ('ENTERPRISE', 'Enterprise')
    # )

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # membership = models.CharField(max_length=25, choices=MEMBERSHIP, default='BASIC')
    # membership = models.ForeignKey(Membership, default=get_basic_membership,
    #                                on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, default=Membership.get_default_pk(),
                                   on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.email}"


class Image(models.Model):
    """Image Model"""

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_file_path)
    image_1 = models.ImageField(upload_to=image_file_path_1, blank=True)
    image_2 = models.ImageField(upload_to=image_file_path_2, blank=True)
    created = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_1 = Img.open(self.image.path)
        img_2 = Img.open(self.image.path)

        output_size_1 = (user.membership.image_1_width,
                         user.membership.image_1_height)
        output_size_2 = (user.membership.image_2_width,
                         user.membership.image_2_height)
        img_1.thumbnail(output_size_1)
        img_2.thumbnail(output_size_2)
        img_1.save(self.image_1.path)
        img_2.save(self.image_2.path)
