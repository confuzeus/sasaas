from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker

from {{ cookiecutter.project_slug }}.accounts.models import TrialRecord
from {{ cookiecutter.project_slug }}.accounts.utils import expire_trial

fake = Faker()
User = get_user_model()


class UtilsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")
        user = User.objects.create(username=fake.user_name(), email=fake.ascii_email())
        cls.user = user
        trial_record = TrialRecord.objects.create(
            user=user, membership_code=TrialRecord.MEMBERSHIP_CODE_CHOICES[0][0]
        )
        cls.trial_record = trial_record

    def test_expire_trial(self):

        expire_trial(999)

        expire_trial(self.trial_record.pk)
        self.trial_record.refresh_from_db()
        self.assertFalse(self.trial_record.expired)

        past = timedelta(days=-365)
        self.trial_record.date = timezone.now() + past
        self.trial_record.save()

        expire_trial(self.trial_record.pk)
        self.trial_record.refresh_from_db()
        self.assertTrue(self.trial_record.expired)
