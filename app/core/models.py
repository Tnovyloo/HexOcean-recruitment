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
    """Generate file path for new Image 1"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'images', '1', filename)

def image_file_path_2(instance, filename):
    """Generate file path for new Image 2"""
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

    image = models.ImageField(upload_to=image_file_path, blank=False)
    image_1 = models.ImageField(upload_to=image_file_path_1, blank=True)
    image_2 = models.ImageField(upload_to=image_file_path_2, blank=True)

    created = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} | {self.title} | {self.user.membership}"

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)

        # If BASIC user saves it.
        if self.image_1:

            self.image = self.image_1
            self.image_2 = self.image_1

            img_1 = Img.open(self.image_1.path)
            img_2 = Img.open(self.image_1.path)
            # img_org = Img.open(self.image_1.path)

            # TODO REPAIR THE OVERRIDE OF SAVE METHOD.
            output_size_1 = (self.user.membership.image_1_width,
                             self.user.membership.image_1_height)

            if self.user.membership.image_2_width and self.user.membership.image_2_height != 0:
                output_size_2 = (self.user.membership.image_2_width,
                                 self.user.membership.image_2_height)
                img_2.thumbnail(output_size_2)
                img_2.save(self.image_2.path)

            img_1.thumbnail(output_size_1)

            # img_org.save(self.image.path)
            img_1.save(self.image_1.path)

