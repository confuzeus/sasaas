from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):
    def _create_membership_groups(self):
        self.stdout.write("Creating membership groups.")
        for group_data in settings.MEMBERSHIP_GROUPS.values():
            group_name = group_data["group_name"]
            Group.objects.get_or_create(name=group_name)
            self.stdout.write(f'Created group named "{group_name}".')

    def _init_user_groups(self):
        """
        Users who aren't part of any memberhsips will be
        added to the default one.
        """
        group_names = [
            group_data["group_name"]
            for group_data in settings.MEMBERSHIP_GROUPS.values()
        ]
        default_group = Group.objects.get(
            name=settings.DEFAULT_MEMBERSHIP_GROUP["group_name"]
        )
        for user in User.objects.all():
            user_group_names = [group.name for group in user.groups.all()]
            common = list(set(group_names) & set(user_group_names))

            if len(common) == 0:
                self.stdout.write(f'Adding user "{user.email}" to default group.')
                user.groups.add(default_group)

    def handle(self, *args, **options):
        self._create_membership_groups()
        self._init_user_groups()
