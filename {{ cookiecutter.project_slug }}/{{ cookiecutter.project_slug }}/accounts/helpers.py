from django.conf import settings


def get_available_trials() -> list:
    trials = []

    for code, group_data in settings.MEMBERSHIP_GROUPS.items():
        if group_data["trial"]["enabled"]:
            trials.append({"code": code, "data": group_data})

    return trials
