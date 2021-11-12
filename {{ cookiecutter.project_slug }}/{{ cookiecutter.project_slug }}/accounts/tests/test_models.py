from decimal import Decimal
from faker import Faker
from django.test import TestCase
from django.contrib.auth import get_user_model
from {{ cookiecutter.project_slug }}.accounts.models import MembershipType, Membership

User = get_user_model()

fake = Faker()


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        membership_type = MembershipType.objects.create(
            name="Pro",
            code="pro",
            price=Decimal(19.99),
        )
        cls.membership_type = membership_type

        user = User(username=fake.user_name(), email=fake.ascii_email())
        user.save()
        cls.user = user

    def test_membership_type(self):

        self.assertEqual(str(self.membership_type), self.membership_type.name)

    def test_membership(self):

        # Default membership created from signal
        self.assertIsNotNone(self.user.membership)

        self.assertEqual(
            str(self.user.membership),
            f"{self.user.username} - {self.user.membership.membership_type.name}",
        )
