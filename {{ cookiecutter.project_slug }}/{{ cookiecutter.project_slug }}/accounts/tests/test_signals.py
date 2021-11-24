from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse_lazy
from faker import Faker

fake = Faker()
User = get_user_model()


class SignalsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")
        user = User.objects.create(username=fake.user_name(), email=fake.ascii_email())
        user.profile.country = "MU"
        user.profile.save()
        cls.user = user

    def test_update_trial_membership(self):

        self.client.force_login(self.user)
        self.client.post(
            reverse_lazy(
                "accounts:activate_trial",
                kwargs={"membership_code": settings.PRO_MEMBERSHIP_CODE},
            )
        )
        self.user.refresh_from_db()
        trial_record = self.user.trial_records.first()
        trial_record.expired = True
        trial_record.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.membership_code, settings.STANDARD_MEMBERSHIP_CODE)
