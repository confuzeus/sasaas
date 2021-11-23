import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.tasks import schedule

from {{ cookiecutter.project_slug }}.accounts.models import TrialRecord, CreditWallet, UserProfile

User = get_user_model()

log = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_post_save_actions(sender, instance, created, **kwargs):

    if created:

        # Membership
        instance.set_membership(settings.DEFAULT_MEMBERSHIP_CODE)
        log.info(f'Added user "{instance.email}" to default membership group.')

        # Credit wallet
        wallet = CreditWallet(user=instance)
        wallet.full_clean()
        wallet.save()
        log.info(f"Created {str(wallet)}")

        # User profile
        profile = UserProfile(user=instance, country=None)
        profile.save()
        log.info(f"Created {str(profile)}")


@receiver(post_save, sender=TrialRecord)
def update_trial_membership(sender, instance, created, **kwargs):

    if created:
        instance.user.set_membership(instance.membership_code)
        schedule(
            "my_awesome_project.accounts.utils.expire_trial",
            instance.pk,
            name=f"Expire {str(instance)}",
            schedule_type="O",
            next_run=instance.expiry_date,
        )
    else:
        if instance.expired:
            instance.user.set_membership(settings.DEFAULT_MEMBERSHIP_CODE)
