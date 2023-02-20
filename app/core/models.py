"""Models for app"""

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from PIL import Image
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

def image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'images', filename)


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

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    membership = models.CharField(max_length=25, choices=MEMBERSHIP, default='BASIC')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.user.email}"


class Image(models.Model):
    """Image Model"""

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_file_path)
    created = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    ## TODO CREATE OWN SAVE METHOD TO SAVE IMAGES IN SPECIFIC DIMENSIONS
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #