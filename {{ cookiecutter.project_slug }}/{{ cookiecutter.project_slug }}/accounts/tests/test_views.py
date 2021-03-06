import unittest.mock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from faker import Faker

from {{ cookiecutter.project_slug }}.accounts import views as accounts_views
from {{ cookiecutter.project_slug }}.accounts.forms import UserProfileForm


User = get_user_model()

fake = Faker()


class AccountsViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("init_membership")
        user = User.objects.create(username=fake.user_name(), email=fake.ascii_email())
        user.profile.country = "MU"
        user.profile.save()
        cls.user = user

    def _assert_redirected_to_login(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url.split("?")[0], reverse_lazy(settings.LOGIN_URL))

    def test_user_settings(self):

        # Unauthenticated requests should redirect to LOGIN_URL
        response = self.client.get(reverse_lazy("accounts:user-settings"))

        self._assert_redirected_to_login(response)

        # Authenticated requests should render properly
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("accounts:user-settings"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response, TemplateResponse))
        self.assertTemplateUsed(response, "accounts/settings.html")

    def test_user_update(self):

        # Unauthenticated requests should redirect to LOGIN_URL
        response = self.client.get(reverse_lazy("accounts:user-update"))

        self._assert_redirected_to_login(response)

        self.client.force_login(self.user)

        # Get requests to should have form's instance set to authed user.
        response = self.client.get(reverse_lazy("accounts:user-update"))
        form = response.context.get("form")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.instance, self.user)
        self.assertFalse(form.is_bound)

        self.assertTemplateUsed(response, "accounts/personal_form.html")

        # Invalid forms should be re-rendered
        with unittest.mock.patch.object(accounts_views, "accounts_forms") as mock:
            instance = mock.UserPersonalInfoForm.return_value
            instance.is_valid.return_value = False
            response = self.client.post(
                reverse_lazy("accounts:user-update"),
                data={"first_name": "", "last_name": ""},
            )
            form = response.context.get("form")
            self.assertTrue(form.is_bound)

        # Valid forms should update user
        self.client.post(
            reverse_lazy("accounts:user-update"),
            data={"first_name": "a", "last_name": "b"},
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "a")
        self.assertEqual(self.user.last_name, "b")

    def test_upgrade_membership(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("accounts:upgrade"))
        self.assertTemplateUsed(response, "accounts/upgrade.html")

        response = self.client.post(
            reverse_lazy("accounts:upgrade"),
            {"upgrade_to": settings.PRO_MEMBERSHIP_CODE},
        )
        self.assertEqual(response.status_code, 200)
    
    def test_activate_trial(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy(
                "accounts:activate_trial",
                kwargs={"membership_code": settings.PRO_MEMBERSHIP_CODE},
            )
        )
        self.assertTrue(response.url, str(settings.UPGRADE_URL))

        response = self.client.post(
            reverse_lazy(
                "accounts:activate_trial",
                kwargs={"membership_code": settings.PRO_MEMBERSHIP_CODE},
            )
        )
        self.assertTrue(response.url, str(settings.LOGIN_REDIRECT_URL))

    def test_wallet_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("accounts:wallet"))
        self.assertTemplateUsed(response, template_name="accounts/wallet.html")

        response = self.client.get(reverse("accounts:wallet") + "?success=True")
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_update_user_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("accounts:update-profile"))
        self.assertTemplateUsed(response, "accounts/update_profile.html")
        self.assertIsInstance(response.context["form"], UserProfileForm)

        response = self.client.post(
            reverse_lazy("accounts:update-profile"), data={"country": "AU"}
        )
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse("accounts:user-settings"))
