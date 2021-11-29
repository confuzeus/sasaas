import base64
import unittest.mock
from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse_lazy
from faker import Faker

from {{ cookiecutter.project_slug }}.payments.utils import Paddle

fake = Faker()
User = get_user_model()


class ViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")
        user = User.objects.create(username=fake.user_name(), email=fake.ascii_email())
        cls.user = user

        cls.paddle_data = {
            "p_signature": base64.b64encode(b"hjdjchdfrfg"),
            "p_currency": "$",
            "p_product_id": settings.PADDLE_CREDIT_PACK_PRODUCT_ID,
            "p_order_id": "5555",
            "p_quantity": "1",
            "p_price": "997",
            "email": user.email,
        }

    def test_paddle_webhook(self):
        with unittest.mock.patch.object(Paddle, "is_valid") as mock:
            mock.return_value = True
            response = self.client.post(
                reverse_lazy("payments:paddle-webhook"), data=self.paddle_data
            )

            self.assertEqual(response.status_code, 200)

            mock.return_value = False

            response = self.client.post(
                reverse_lazy("payments:paddle-webhook"), data=self.paddle_data
            )

            self.assertEqual(response.status_code, 400)

        response = self.client.get(reverse_lazy("payments:paddle-webhook"))
        self.assertEqual(response.status_code, 400)
