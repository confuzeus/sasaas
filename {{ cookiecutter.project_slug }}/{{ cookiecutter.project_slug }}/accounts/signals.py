import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

log = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def add_user_to_membership_group(sender, instance, created, **kwargs):

    if created:
        instance.set_membership(settings.DEFAULT_MEMBERSHIP_CODE)
        log.info(f'Added user "{instance.email}" to default membership group.')
