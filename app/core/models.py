"""Models for app"""

import sys
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from PIL import Image as Img
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.core.files.base import ContentFile
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
    """Manager for users."""

    def create_user(self, email, password=None, **extra_field):
        """Create, save and return a new user"""

        if not email:
            raise ValueError("User must have an email address!")

        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

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
    image_1_height = models.IntegerField(null=False, default=200)
    image_1_width = models.IntegerField(null=False, default=200)
    image_2_height = models.IntegerField(null=True, blank=True, default=400)
    image_2_width = models.IntegerField(null=True, blank=True, default=400)
    is_able_to_create_url = models.BooleanField(default=False)

    def __str__(self):
        return self.tier_name

    # @classmethod
    # def get_default_pk(cls):
    #     tier, created = cls.objects.get_or_create(
    #         tier_name="BASIC",
    #         image_1_height=200,
    #         image_1_width=200,
    #     )
    #     return tier.pk


class User(AbstractBaseUser, PermissionsMixin):
    """Model for the user in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # membership = models.ForeignKey(Membership, default=Membership.get_default_pk(),
    #                                on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, blank=True, null=True)

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
        return f"{self.user.email} - {self.title}"

    def save(self, *args, **kwargs):
        """Override save method to save images in all resolution if membership permits"""

        if not self.make_thumbnails():
            raise Exception("Could not create thumbnail")

        super(Image, self).save(*args, **kwargs)

    def make_thumbnails(self):
        """Make thumbnails method."""
        image_1 = Img.open(self.image_1)


        OUTPUT_SIZE_1 = (self.user.membership.image_1_width,
                         self.user.membership.image_1_height)

        # IF USER MEMBERSHIP IS NOT BASIC
        if self.user.membership.tier_name != "BASIC":
            # SAVE IMAGE 2 ( DEFAULT IN 400PX )
            image_2 = Img.open(self.image_1)
            OUTPUT_SIZE_2 = (self.user.membership.image_2_width,
                             self.user.membership.image_2_height
                             )
            image_2.thumbnail(OUTPUT_SIZE_2, Img.ANTIALIAS)
            thumb_2_name, thumb_2_extension = os.path.splitext(self.image_1.name)
            thumb_2_extension = thumb_2_extension.lower()

            thumb_2_filename = thumb_2_name + "_thumb2" + thumb_2_extension

            if thumb_2_extension in ['.jpg', '.jpeg']:
                FTYPE = 'JPEG'
            elif thumb_2_extension == '.png':
                FTYPE = 'PNG'
            else:
                return False  # Unrecognized file type

            temp_thumb_2 = BytesIO()
            image_2.save(temp_thumb_2, FTYPE)
            temp_thumb_2.seek(0)

            self.image_2.save(thumb_2_filename, ContentFile(temp_thumb_2.read()), save=False)
            temp_thumb_2.close()

            # SAVE ORIGINAL PHOTO
            image = Img.open(self.image_1)
            image_name, image_extension = os.path.splitext(self.image_1.name)
            image_extension = image_extension.lower()

            image_filename = image_name + '_original' + image_extension
            if image_extension in ['.jpg', '.jpeg']:
                FTYPE = 'JPEG'
            elif image_extension == '.png':
                FTYPE = 'PNG'
            else:
                return False

            temp_image = BytesIO()
            image.save(temp_image, FTYPE)
            temp_image.seek(0)

            self.image.save(image_filename, ContentFile(temp_image.read()), save=False)
            temp_image.close()

        # SAVING IMAGE 1

        image_1.thumbnail(OUTPUT_SIZE_1, Img.ANTIALIAS)

        thumb_1_name, thumb_1_extension = os.path.splitext(self.image_1.name)
        thumb_1_extension = thumb_1_extension.lower()

        thumb_1_filename = thumb_1_name + '_thumb1' + thumb_1_extension

        if thumb_1_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_1_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        temp_thumb_1 = BytesIO()
        image_1.save(temp_thumb_1, FTYPE)
        temp_thumb_1.seek(0)

        self.image_1.save(thumb_1_filename, ContentFile(temp_thumb_1.read()), save=False)
        temp_thumb_1.close()

        return True


class URLExpiration(models.Model):
    """Model for URL expiration"""

    image = models.ForeignKey(Image, on_delete=models.CASCADE, blank=False)
    url = models.CharField(max_length=255)
    time = models.IntegerField(blank=False)

    def save(self, *args, **kwargs):
        self.url = self.image.image.url
        super(URLExpiration, self).save(*args, **kwargs)
