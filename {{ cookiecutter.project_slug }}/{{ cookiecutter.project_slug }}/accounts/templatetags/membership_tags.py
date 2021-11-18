from django import template
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured

from {{ cookiecutter.project_slug }}.accounts.helpers import get_available_trials
from {{ cookiecutter.project_slug }}.accounts.models import TrialRecord

register = template.Library()

User = get_user_model()


@register.simple_tag()
def get_trials_for_user(user: User) -> list:
    """
    Get the trials a user is allowed to activate.
    """
    trials = get_available_trials()
    for index, trial in enumerate(trials):
        try:
            TrialRecord.objects.get(user=user, membership_code=trial["code"])
            trials.pop(index)
        except TrialRecord.DoesNotExist:
            pass

    return trials


@register.simple_tag()
def get_trial_message(code: str) -> str:
    group_data = settings.MEMBERSHIP_GROUPS[code]

    period = group_data["trial"]["period"]

    term = period[-1]
    term_length = int(period[:-1])

    if term == "d":
        term_verbose = "day"
    elif term == "m":
        term_verbose = "month"
    elif term == "y":
        term_verbose = "year"
    else:
        raise ImproperlyConfigured('Terms can be either "d", "m", or "y".')

    if term_length > 1:
        term_verbose += "s"

    message = f"Try {group_data['name']} free for {term_length} {term_verbose}"
    return message
