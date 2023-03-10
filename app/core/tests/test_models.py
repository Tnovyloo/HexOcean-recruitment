"""Tests for models"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files import File
from django.urls import reverse

from io import BytesIO
from PIL import Image
from django.core.files.base import File


from core import models

from unittest.mock import patch
import uuid

def create_user(email='user@example.com', password='testpass123', membership=None):
    if membership is not None:
        user = get_user_model().objects.create_user(email, password)

        membership_model = models.Membership.objects.get_or_create(tier_name=membership,
                                                            image_1_height = 200,
                                                            image_1_width = 200,
                                                            )
        user.membership = membership_model[0]
        return user


    user = get_user_model().objects.create_user(email, password)

    basic = models.Membership.objects.get_or_create(tier_name="BASIC",
                                             image_1_height=200,
                                             image_1_width=200)

    user.membership = basic[0]
    # print(basic)
    # print(basic[0])
    return user

def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
    file_obj = StringIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a Value Error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')


    def test_create_user_with_membership(self):
        """Test user memberships"""
        # New user is by default assigned to Basic class.
        user = create_user()
        self.assertEqual(user.membership.tier_name, "BASIC")

        user = create_user(email='sample123123@example.com', membership="PREMIUM")
        self.assertEqual(user.membership.tier_name, "PREMIUM")

        user = create_user(email='samp@example.com', membership="ENTERPRISE")
        self.assertEqual(user.membership.tier_name, "ENTERPRISE")



    @patch('core.models.uuid.uuid4')
    def test_image_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        file_path = models.image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/images/original/{uuid}.jpg')

    @patch('core.models.uuid.uuid4')
    def test_image_file_name_1_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        file_path = models.image_file_path_1(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/images/1/{uuid}.jpg')

    @patch('core.models.uuid.uuid4')
    def test_image_file_name_2_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        file_path = models.image_file_path_2(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/images/2/{uuid}.jpg')

