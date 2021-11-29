from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker

fake = Faker()
User = get_user_model()


class MiddlewareTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")
        user = User.objects.create(username=fake.user_name(), email=fake.ascii_email())
        cls.user = user

    def test_complete_user_profile_middleware(self):
        self.client.force_login(self.user)
        response = self.client.get("/")
        self.assertEqual(response.url, reverse("accounts:update-profile") + "?next=/")

        self.user.profile.country = "MU"
        self.user.profile.save()
        response = self.client.get("/")
        self.assertEqual(response.request["PATH_INFO"], "/")
