from django.test import TestCase

from user.models import User


class TestUser(TestCase):
    """test user model"""

    @classmethod
    def setUpTestData(cls):
        test_user_1 = User.objects.create(email="django_test_user_1@xyz.com", password="mr.goose", type="user")
        test_user_1.save()
        test_user_2 = User.objects.create(email="django_test_user_2@xyz.com", password="mrs.goose", type="admin")
        test_user_2.save()
        test_user_3 = User.objects.create(email="django_test_user_3@xyz.com", password="miss.goose")
        test_user_3.save()

    def test_email_label(self):
        user = User.objects.get(email="django_test_user_1@xyz.com")
        field_label = user._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "email")

    def test_password_label(self):
        user = User.objects.get(email="django_test_user_1@xyz.com")
        field_label = user._meta.get_field("password").verbose_name
        self.assertEqual(field_label, "password")

    def test_type_label(self):
        user = User.objects.get(email="django_test_user_1@xyz.com")
        field_label = user._meta.get_field("type").verbose_name
        self.assertEqual(field_label, "type")

    def test_email_max_length(self):
        user = User.objects.get(email="django_test_user_1@xyz.com")
        max_length = user._meta.get_field("email").max_length
        self.assertEqual(max_length, 128)

    def test_password_max_length(self):
        user = User.objects.get(email="django_test_user_1@xyz.com")
        max_length = user._meta.get_field("password").max_length
        self.assertEqual(max_length, 64)

    def test_type_user(self):
        user = User.objects.get(email="django_test_user_1@xyz.com")
        user_type = user.type
        self.assertEqual(user_type, "user")

    def test_type_admin(self):
        user = User.objects.get(email="django_test_user_2@xyz.com")
        user_type = user.type
        self.assertEqual(user_type, "admin")

    def test_default_type(self):
        user = User.objects.get(email="django_test_user_3@xyz.com")
        user_type = user.type
        self.assertEqual(user_type, "user")

    def test_type_max_length(self):
        user = User.objects.get(email="django_test_user_1@xyz.com")
        max_length = user._meta.get_field("type").max_length
        self.assertEqual(max_length, 16)

    def test_create_user_twice(self):
        pass
