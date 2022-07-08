from django.test import TestCase
from django.contrib.auth import get_user_model


class UsersManagersTests(TestCase):
    """
    Before create custom_admin:
    make sure the tests fail:
    TypeError: create_superuser() missing 1 required positional argument: 'username'

    After create custom_admin:
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.275s

    OK
    """
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='student@user.com', password='123456')
        self.assertEqual(user.email, 'student@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="123456")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', password='123456')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='123456', is_superuser=False)