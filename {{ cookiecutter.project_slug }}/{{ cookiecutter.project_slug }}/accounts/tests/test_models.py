from decimal import Decimal
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.exceptions import ValidationError
from faker import Faker
from django.test import TestCase
from django.contrib.auth import get_user_model
from my_awesome_project.accounts.models import MembershipType, Membership

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

        # Group was created from signal
        group = Group.objects.filter(name=self.membership_type.name).first()
        self.assertIsNotNone(group)

    def test_membership(self):

        # Default membership created from signal
        self.assertIsNotNone(self.user.membership)

        self.assertEqual(
            str(self.user.membership),
            f"{self.user.username} - {settings.DEFAULT_MEMBERSHIP_NAME}",
        )

        # One membership per user.
        membership = Membership(membership_type=self.membership_type, user=self.user)
        with self.assertRaises(ValidationError):
            membership.full_clean()

        self.user.refresh_from_db()

        # User was added to group
        group = self.user.groups.filter(name=self.membership_type.name)
        self.assertIsNotNone(group)

        # User's group changed by signal
        self.user.membership.membership_type = self.membership_type
        self.user.membership.save()
        new_group_names = [group.name for group in self.user.groups.all()]
        self.assertNotIn(settings.DEFAULT_MEMBERSHIP_NAME, new_group_names)
