from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):
    def _create_membership_groups(self):
        self.stdout.write("Creating membership groups.")
        for group_name in settings.MEMBERSHIP_GROUPS.values():
            Group.objects.get_or_create(name=group_name)
            self.stdout.write(f'Created group named "{group_name}".')

    def _init_user_groups(self):
        """
        Users who aren't part of any memberhsips will be
        added to the default one.
        """
        group_names = settings.MEMBERSHIP_GROUPS.values()
        default_group = Group.objects.get(name=settings.DEFAULT_MEMBERSHIP_GROUP)
        for user in User.objects.all():
            user_group_names = [group.name for group in user.groups.all()]
            found = False
            for user_group in user_group_names:
                if user_group in group_names:
                    found = True
                    break

            if not found:
                self.stdout.write(f'Adding user "{user.email}" to default group.')
                user.groups.add(default_group)

    def handle(self, *args, **options):
        self._create_membership_groups()
        self._init_user_groups()
