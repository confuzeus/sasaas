from functools import cached_property
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group

from {{ cookiecutter.project_slug }}.accounts.exceptions import MultipleMemberships, NoMembership


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
