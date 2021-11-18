from django.conf import settings


def site_data(request):
    return {
        "django_debug": settings.DEBUG,
        "captcha_site_key": settings.CAPTCHA_SITE_KEY,
        "allow_registration": settings.ACCOUNT_ALLOW_REGISTRATION,
        "membership_codes": {
            "standard": settings.STANDARD_MEMBERSHIP_CODE,
            "pro": settings.PRO_MEMBERSHIP_CODE,
        },
    }
