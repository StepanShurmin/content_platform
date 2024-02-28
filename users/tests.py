from django.core.management import call_command
from django.test import TestCase, Client

from users.models import User


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(
            first_name="Test", last_name="Testov", phone="89221234566", username="test"
        )
        cls.user_1.set_password("123")
        cls.user_1.save()
        cls.user_2 = User.objects.create(
            first_name="Test2",
            last_name="Testov",
            phone="89221234568",
            username="test2",
        )
        cls.user_2.subscriptions.add(cls.user_1)
        cls.user_2.set_password("1234")
        cls.user_2.save()

    def test_login(self):
        client = Client()
        response = client.post(
            "/user/login/", {"phone": "89221234566", "password": "123"}
        )
        self.assertEqual(response.status_code, 200)

    def test_my_profile(self):
        client = Client()
        client.login(phone="89221234566", password="123")
        response = client.get("/user/my_profile")
        self.assertEqual(response.status_code, 200)
        self.assertIn("89221234566", response.content.decode())
        self.assertIn("test", response.content.decode())
        self.assertIn("Test Testov", response.content.decode())
        self.assertIn("нет подписок", response.content.decode())
        self.assertIn("Testov Test2", response.content.decode())

    def test_super_user_created(self):
        call_command("csu")
        superuser = User.objects.get(username="admin")

        self.assertEqual(superuser.phone, "89221234567")
        self.assertEqual(superuser.first_name, "Admin")
        self.assertEqual(superuser.last_name, "SkyPro")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password("123"))
