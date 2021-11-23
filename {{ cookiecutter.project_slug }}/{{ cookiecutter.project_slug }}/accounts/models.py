from datetime import datetime
from functools import cached_property

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django_countries.fields import CountryField

from {{ cookiecutter.project_slug }}.accounts.exceptions import MultipleMemberships, NoMembership
from {{ cookiecutter.project_slug }}.accounts.helpers import get_available_trials


class User(AbstractUser):
    def set_membership(self, code: str):
        new_group = Group.objects.get(
            name=settings.MEMBERSHIP_GROUPS[code]["group_name"]
        )
        try:
            old_group = Group.objects.get(
                name=settings.MEMBERSHIP_GROUPS[self.membership_code]["group_name"]
            )
            self.groups.remove(old_group)
        except Group.DoesNotExist:
            pass
        except NoMembership:
            pass

        self.groups.add(new_group)
        self.clear_membership_cache()

    def clear_membership_cache(self):
        try:
            del self.__dict__["membership_code"]
            del self.__dict__["membership_name"]
        except KeyError:
            pass

    @cached_property
    def membership_code(self) -> str:
        code = ""
        for group_code, group_data in settings.MEMBERSHIP_GROUPS.items():
            group_name = group_data["group_name"]
            if group_name == self.membership_name:
                code = group_code
                break
        return code

    @cached_property
    def membership_name(self) -> str:
        user_group_names = [group.name for group in self.groups.all()]
        all_membership_groups = [
            group_data["group_name"]
            for group_data in settings.MEMBERSHIP_GROUPS.values()
        ]

        common = list(set(user_group_names) & set(all_membership_groups))

        if len(common) > 1:
            raise MultipleMemberships(
                "A user can be part of a single membership group."
            )

        if len(common) == 0:
            raise NoMembership("A user must be part of at least one membership.")

        return common[0]


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    country = CountryField(null=True)

    def __str__(self):
        return f"{self.user.email}'s profile."


class TrialRecord(models.Model):
    MEMBERSHIP_CODE_CHOICES = [
        (trial["code"], trial["data"]["name"]) for trial in get_available_trials()
    ]
    user: User = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trial_records"
    )
    membership_code = models.CharField(max_length=40, choices=MEMBERSHIP_CODE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "membership_code"], name="unique_trial_user_membership"
            )
        ]

    def __str__(self):
        return f"Trial: {self.user.email} for {self.membership_code}."

    @cached_property
    def expiry_date(self) -> datetime:
        """
        Get the expiry `datetime` given period as specified in settings.MEMBERSHIP_GROUPS
        """
        period = settings.MEMBERSHIP_GROUPS[self.membership_code]["trial"]["period"]
        term = period[-1]
        term_length = int(period[:-1])

        if term == "d":
            future = relativedelta(days=term_length)
        elif term == "m":
            future = relativedelta(months=term_length)
        elif term == "y":
            future = relativedelta(years=term_length)
        else:
            raise ImproperlyConfigured("Period must be either d, m, or y.")

        return self.date + future


class CreditWallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="credit_wallet"
    )
    credits = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s wallet."
