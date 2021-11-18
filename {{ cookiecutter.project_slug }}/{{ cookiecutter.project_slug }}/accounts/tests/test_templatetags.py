import unittest.mock

from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from faker import Faker
from django.test import TestCase, RequestFactory

from {{ cookiecutter.project_slug }}.accounts.helpers import get_available_trials
from {{ cookiecutter.project_slug }}.accounts.templatetags.membership_tags import (
    get_trials_for_user,
    get_trial_message,
)
from {{ cookiecutter.project_slug }}.accounts.templatetags.membership_tags import (
    settings as membership_tags_settings,
)

User = get_user_model()
fake = Faker()


class TemplateTagsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")
        user = User.objects.create(username=fake.user_name(), email=fake.ascii_email())
        cls.user = user

        cls.factory = RequestFactory()

    def test_membership_tags(self):
        all_trials = get_available_trials()

        # User should not have activated any trials yet
        trials = get_trials_for_user(self.user)
        self.assertEqual(len(trials), len(all_trials))

        self.client.force_login(self.user)

        # Activate pro trial
        self.client.post(
            reverse_lazy(
                "accounts:activate_trial",
                kwargs={"membership_code": settings.PRO_MEMBERSHIP_CODE},
            )
        )
        trials = get_trials_for_user(self.user)
        self.assertGreater(len(all_trials), len(trials))

        call_command("init_membership")

        def get_message(group_name: str, trial_data: dict) -> str:
            period = trial_data["period"]

            term = period[-1]
            term_length = int(period[:-1])

            if term == "d":
                term_verbose = "day"
            elif term == "m":
                term_verbose = "month"
            else:
                term_verbose = "year"

            if term_length > 1:
                term_verbose += "s"

            return f"Try {group_name} free for {term_length} {term_verbose}"

        with unittest.mock.patch.object(
            membership_tags_settings, "MEMBERSHIP_GROUPS"
        ) as mock:
            groups = {
                fake.word(): {
                    "name": fake.word(),
                    "group_name": fake.word(),
                    "recurring": True,
                    "trial": {
                        "enabled": True,
                        "period": "1d",
                    },
                    "period": "30d",
                },
                fake.word(): {
                    "name": fake.word(),
                    "group_name": fake.word(),
                    "recurring": True,
                    "trial": {
                        "enabled": True,
                        "period": "1m",
                    },
                    "period": "30d",
                },
                fake.word(): {
                    "name": fake.word(),
                    "group_name": fake.word(),
                    "recurring": True,
                    "trial": {
                        "enabled": True,
                        "period": "1y",
                    },
                    "period": "30d",
                },
                fake.word(): {
                    "name": fake.word(),
                    "group_name": fake.word(),
                    "recurring": True,
                    "trial": {
                        "enabled": True,
                        "period": "14d",
                    },
                    "period": "30d",
                },
            }

            mock.__getitem__.side_effect = groups.__getitem__

            for code, data in groups.items():
                self.assertEqual(
                    get_message(data["name"], data["trial"]), get_trial_message(code)
                )

            fake_code = fake.word()
            groups = {
                fake_code: {
                    "name": fake.word(),
                    "group_name": fake.word(),
                    "recurring": True,
                    "trial": {
                        "enabled": True,
                        "period": "14l",
                    },
                    "period": "30d",
                },
            }

            mock.__getitem__.side_effect = groups.__getitem__

            with self.assertRaises(ImproperlyConfigured):
                get_trial_message(fake_code)
