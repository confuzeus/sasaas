from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.test import TestCase
from faker import Faker

User = get_user_model()

fake = Faker()


class ManagementTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")
        user = User.objects.create(username=fake.user_name(), email=fake.ascii_email())
        cls.user = user

    def test_init_site(self):
        call_command("init_site")

        site = Site.objects.first()
        self.assertEqual(site.name, settings.PROJECT_NAME)
        self.assertEqual(site.domain, f"{settings.DOMAIN_NAME}:{settings.PORT_NUMBER}")

    def test_init_membership(self):
        for group_data in settings.MEMBERSHIP_GROUPS.values():
            group_name = group_data["group_name"]
            group = Group.objects.filter(name=group_name).first()
            self.assertIsNotNone(group)

        group_names = [group.name for group in self.user.groups.all()]
        self.assertIn(settings.DEFAULT_MEMBERSHIP_GROUP["group_name"], group_names)
