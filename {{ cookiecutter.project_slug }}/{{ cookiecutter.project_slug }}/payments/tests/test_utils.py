import base64
import unittest.mock
from unittest.mock import MagicMock
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from faker import Faker
from django.contrib.auth import get_user_model

from {{ cookiecutter.project_slug }}.payments import utils as payment_utils
from {{ cookiecutter.project_slug }}.payments.models import Payment

User = get_user_model()
fake = Faker()


class UtilsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")
        user_email = fake.ascii_email()
        user = User.objects.create(username=fake.user_name(), email=user_email)
        user.profile.country = "MU"
        user.profile.save()
        cls.user = user

        paddle_data = {
            "p_signature": base64.b64encode(b"hjdjchdfrfg"),
            "p_currency": "$",
            "p_product_id": "1234",
            "p_order_id": "5555",
            "p_quantity": "1",
            "p_price": "997",
            "email": user_email,
        }
        cls.paddle_data = paddle_data

    def test_paddle(self):
        paddle = payment_utils.Paddle(self.paddle_data)

        self.assertFalse(paddle.is_valid)

        with unittest.mock.patch.object(payment_utils, "PKCS1_v1_5") as mock:

            verifier = MagicMock()
            mock.new.return_value = verifier

            verifier.verify.return_value = True

            paddle = payment_utils.Paddle(self.paddle_data)

            self.assertTrue(paddle.is_valid)

            paddle.record_payment(settings.CREDIT_PRODUCT_CODE)

            payment = Payment.objects.filter(
                product_code=settings.CREDIT_PRODUCT_CODE
            ).first()

            self.assertIsNotNone(payment)

            paddle.add_credits()

            self.user.refresh_from_db()
            self.assertEqual(
                self.user.credit_wallet.credits, settings.PADDLE_CREDITS_PER_PACK
            )
