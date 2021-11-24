import logging
from django.conf import settings
from allauth.account import forms as allauth_account_forms
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from {{ cookiecutter.project_slug }}.accounts.models import TrialRecord, UserProfile
from {{ cookiecutter.project_slug }}.core.mixins.form_mixins import HcaptchaFormMixin

User = get_user_model()

log = logging.getLogger(__name__)


class LoginForm(HcaptchaFormMixin, allauth_account_forms.LoginForm):
    pass


class ResetPasswordForm(HcaptchaFormMixin, allauth_account_forms.ResetPasswordForm):
    pass


class ResetPasswordKeyForm(
    HcaptchaFormMixin, allauth_account_forms.ResetPasswordKeyForm
):
    pass


class ChangePasswordForm(HcaptchaFormMixin, allauth_account_forms.ChangePasswordForm):
    pass


class SignupForm(HcaptchaFormMixin, allauth_account_forms.SignupForm):
    pass


class UserPersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["country"]


class TrialRecordForm(forms.ModelForm):
    class Meta:
        model = TrialRecord
        fields = ["user", "membership_code"]


class MembershipUpgradeForm(forms.Form):

    upgrade_to = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(MembershipUpgradeForm, self).__init__(*args, **kwargs)

    def clean_upgrade_to(self):
        upgrade_to = self.cleaned_data["upgrade_to"]
        upgrade_paths = settings.UPGRADE_PATHS.get(self.user.membership_code, [])
        if not (upgrade_to in upgrade_paths):
            log.info(
                f'User "{self.user.email}" tried to upgrade to membership coded "{upgrade_to}".'
            )
            raise ValidationError(
                _(
                    "You're not allowed to upgrade to this plan. Please choose another one."
                )
            )

        return upgrade_to
