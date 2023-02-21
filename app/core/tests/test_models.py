"""Tests for models"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core import models

from unittest.mock import patch
import uuid

def create_user(email='user@example.com', password='testpass123', membership=None):
    if membership is not None:
        user = get_user_model().objects.create_user(email, password)
        user.membership = membership
        return user
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email if is it normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = create_user(email=email, password='sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a Value Error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user_with_membership(self):
        """Test user memberships"""
        # New user is by default assigned to Basic class.
        user = create_user()
        self.assertEqual(user.membership, 'BASIC')

        # Testing Premium membership
        user = create_user(email='example123123@example.com')
        user.membership = "PREMIUM"
        user.save()
        self.assertEqual(user.membership, "PREMIUM")

        # Testing Enterprise membership
        user = create_user(email='exam@example.com')
        user.membership = "ENTERPRISE"
        user.save()
        self.assertEqual(user.membership, "ENTERPRISE")

    @patch('core.models.uuid.uuid4')
    def test_image_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        file_path = models.image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/images/original/{uuid}.jpg')

    @patch('core.models.uuid.uuid4')
    def test_image_file_name_uuid_200(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        file_path = models.image_file_path_200(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/images/200/{uuid}.jpg')

    @patch('core.models.uuid.uuid4')
    def test_image_file_name_uuid_400(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        file_path = models.image_file_path_400(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/images/400/{uuid}.jpg')

    # def test_create_image_model(self):
    #     """Tests creating of Image model"""
    #     user = create_user()
    #     image = models.Image.objects.create(title="Image123",
    #                                         user=user)
    #
    #     self.assertEqual("Image123", image.title)
    #     self.assertEqual("Image123", str(image))
    #     self.assertEqual(user, image.user)