from django.contrib.sites.models import Site
from django.test import TestCase
from django.core.management import call_command
from django.conf import settings


class ManagementTests(TestCase):
    def test_init_site(self):
        call_command("init_site")

        site = Site.objects.first()
        self.assertEqual(site.name, settings.PROJECT_NAME)
        self.assertEqual(site.domain, f"{settings.DOMAIN_NAME}:{settings.PORT_NUMBER}")
