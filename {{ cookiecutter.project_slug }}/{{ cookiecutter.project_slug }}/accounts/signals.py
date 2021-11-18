import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.tasks import schedule

from {{ cookiecutter.project_slug }}.accounts.models import TrialRecord

User = get_user_model()

log = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def add_user_to_membership_group(sender, instance, created, **kwargs):

    if created:
        instance.set_membership(settings.DEFAULT_MEMBERSHIP_CODE)
        log.info(f'Added user "{instance.email}" to default membership group.')


@receiver(post_save, sender=TrialRecord)
def update_trial_membership(sender, instance, created, **kwargs):

    if created:
        instance.user.set_membership(instance.membership_code)
        schedule(
            "{{ cookiecutter.project_slug }}.accounts.utils.expire_trial",
            instance.pk,
            name=f"Expire {str(instance)}",
            schedule_type="O",
            next_run=instance.expiry_date,
        )
    else:
        if instance.expired:
            instance.user.set_membership(settings.DEFAULT_MEMBERSHIP_CODE)
