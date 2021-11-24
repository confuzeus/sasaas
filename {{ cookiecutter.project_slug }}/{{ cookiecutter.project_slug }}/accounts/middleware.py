from django.shortcuts import redirect
from django.urls import reverse


class CompleteUserProfileMiddleware:
    """
    Redirect the user to profile update view if it's incomplete.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.split("?")[0] != reverse("accounts:update-profile"):
            if request.user.is_authenticated:

                if not request.user.profile.is_complete:

                    return redirect(
                        reverse("accounts:update-profile")
                        + f"?next={request.path.split('?')[0]}"
                    )

        response = self.get_response(request)
        return response
