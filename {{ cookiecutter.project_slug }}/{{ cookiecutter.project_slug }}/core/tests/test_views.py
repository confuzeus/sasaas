from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from faker import Faker

User = get_user_model()
fake = Faker()


class ViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")

        standard_user = User.objects.create(
            username=fake.user_name(), email=fake.ascii_email()
        )
        cls.standard_user = standard_user

        pro_user = User.objects.create(
            username=fake.user_name(), email=fake.ascii_email()
        )
        pro_user.set_membership(code=settings.PRO_MEMBERSHIP_CODE)
        cls.pro_user = pro_user

    def test_user_access(self):

        response = self.client.get(reverse_lazy("accounts:standard-access"))
        self.assertEqual(response.status_code, 302)
        self.assertRegex(response.url, reverse(settings.LOGIN_URL))

        response = self.client.get(reverse_lazy("accounts:pro-access"))
        self.assertEqual(response.status_code, 302)
        self.assertRegex(response.url, reverse(settings.LOGIN_URL))

        self.client.force_login(self.standard_user)
        response = self.client.get(reverse_lazy("accounts:standard-access"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

        response = self.client.get(reverse_lazy("accounts:pro-access"))
        self.assertEqual(response.status_code, 302)
        if settings.UPGRADE_URL == "/":
            path = response.url.split("?")[0]
            self.assertEqual("/", path)
        else:
            self.assertRegex(response.url, str(settings.UPGRADE_URL))

        self.client.force_login(self.pro_user)
        response = self.client.get(reverse_lazy("accounts:pro-access"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

        response = self.client.get(reverse_lazy("accounts:standard-access"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
