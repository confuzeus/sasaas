from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MembershipType, Membership

User = get_user_model()


@receiver(post_save, sender=User)
def add_user_to_default_membership(sender, instance, created, **kwargs):

    if created:
        membership_type = MembershipType.objects.get(
            code=settings.DEFAULT_MEMBERSHIP_CODE
        )
        membership = Membership(membership_type=membership_type, user=instance)
        membership.full_clean()
        membership.save()


@receiver(post_save, sender=MembershipType)
def create_corresponding_group(sender, instance, created, **kwargs):

    if created:
        group = Group(name=instance.name)
        group.full_clean()
        group.save()
        instance.group = group
        instance.save()


@receiver(post_save, sender=Membership)
def add_user_to_group(sender, instance, **kwargs):

    # Remove existing membership groups first
    membership_type_group_names = [
        membership_type.name for membership_type in MembershipType.objects.all()
    ]

    existing_membership_type_groups = instance.user.groups.filter(
        name__in=membership_type_group_names
    )

    for existing_group in existing_membership_type_groups:
        instance.user.groups.remove(existing_group)

    instance.user.groups.add(instance.membership_type.group)
