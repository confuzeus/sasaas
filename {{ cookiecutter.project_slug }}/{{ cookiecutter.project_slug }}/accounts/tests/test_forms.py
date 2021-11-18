from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from faker import Faker

from {{ cookiecutter.project_slug }}.accounts.forms import MembershipUpgradeForm

User = get_user_model()
fake = Faker()


class FormsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")
        user = User.objects.create(username=fake.user_name(), email=fake.ascii_email())
        cls.user = user

    def test_membership_upgrade_form(self):
        form = MembershipUpgradeForm(
            {"upgrade_to": settings.PRO_MEMBERSHIP_CODE}, user=self.user
        )
        self.assertTrue(form.is_valid())

        form = MembershipUpgradeForm({"upgrade_to": "neine"}, user=self.user)
        self.assertFalse(form.is_valid())
