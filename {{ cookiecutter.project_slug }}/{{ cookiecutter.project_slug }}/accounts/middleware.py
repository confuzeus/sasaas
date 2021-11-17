from django.conf import settings

from {{ cookiecutter.project_slug }}.accounts.exceptions import MultipleMemberships


class UserMembershipMiddleware:
    """
    Adds an authenticated user's membership group name to session.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response
