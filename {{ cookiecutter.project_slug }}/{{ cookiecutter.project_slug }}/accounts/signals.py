from django.conf import settings
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
