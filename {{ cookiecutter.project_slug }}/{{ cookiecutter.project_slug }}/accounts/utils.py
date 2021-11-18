import logging

from django.utils import timezone

from {{ cookiecutter.project_slug }}.accounts.models import TrialRecord

log = logging.getLogger(__name__)


def expire_trial(pk):
    """
    Expire a TrialRecord given it's primary key pk.
    """
    try:
        trial_record = TrialRecord.objects.get(pk=pk)
    except TrialRecord.DoesNotExist:
        log.exception(f"TrialRecord with pk {pk} not found. Unable to expire.")
        return

    now = timezone.now()
    expiry_date = trial_record.expiry_date
    if now > expiry_date:
        trial_record.expired = True
        trial_record.save()
        log.info(f'Trial "{str(trial_record)}" expired.')
