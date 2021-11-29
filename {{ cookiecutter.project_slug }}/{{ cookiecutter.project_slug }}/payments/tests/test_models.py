from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from faker import Faker
from django.conf import settings

from {{ cookiecutter.project_slug }}.payments.models import Payment

fake = Faker()
User = get_user_model()


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")
        user = User.objects.create(username=fake.user_name, email=fake.ascii_email())
        cls.user = user

    def test_payment(self):
        source = "abcd"
        payment = Payment.objects.create(
            user=self.user,
            source=source,
            reference="hjhdfg",
            product_code=settings.PRODUCT_CODE_CHOICES[0][0],
            total=1000,
        )

        self.assertEqual(
            str(payment),
            f"Payment by {self.user.email} using {source} on {payment.date}",
        )
