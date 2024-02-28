from django.test import TestCase, Client

from content.models import Publication
from content.services import (
    create_session,
    create_price,
    create_product,
)
from users.models import User


class PublicationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create(
            first_name="Test", last_name="Testov", phone="89221234567", username="test"
        )
        user_1.set_password("123")
        user_1.save()
        cls.data = {"title": "test_title", "body": "test_content", "is_paid": False}
        cls.post = Publication.objects.create(
            title="title", body="body", is_paid=True, owner=user_1
        )

    def test_create_post(self):
        client = Client()
        client.login(phone="89221234567", password="123")
        response = client.post(
            "/content/create/",
            data={"title": "test_title", "body": "test_content", "is_paid": False},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/content/2/")
        self.assertTrue(Publication.objects.all().exists())

    def test_read_post(self):
        client = Client()
        client.login(phone="89221234567", password="123")
        response = client.get(f"/content/{self.post.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.content.decode())
        self.assertIn("body", response.content.decode())

    def test_update_post(self):
        client = Client()
        client.login(phone="89221234567", password="123")
        response = client.post(
            "/content/update/1/",
            data={
                "title": "new_test_title",
                "body": "new_test_content",
                "is_paid": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/content/1/")

    def test_delete_post(self):
        client = Client()
        client.login(phone="89221234567", password="123")
        response = client.post(
            "/content/delete/1/",
        )
        self.assertEqual(response.status_code, 302)


class StripeTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="testuser", email="test@example.com", password="12345"
        )

    def test_create_product(self):
        product = create_product(self.user)
        self.assertIsNotNone(product)

    def test_create_price(self):
        price = create_price(self.user)
        self.assertIsNotNone(price)

    def test_create_session(self):
        session_url = create_session(self.user)
        self.assertIsNotNone(session_url)
