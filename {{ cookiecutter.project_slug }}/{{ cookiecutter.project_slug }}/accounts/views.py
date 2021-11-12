from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib import messages
from allauth.account.views import PasswordSetView as AllauthPasswordSetView
from django.urls import reverse_lazy

from . import forms as accounts_forms


@login_required
def user_settings(request):
    return TemplateResponse(request, "accounts/settings.html")


@login_required
def user_update(request):
    ctx = {}
    if request.method == "POST":
        form = accounts_forms.UserPersonalInfoForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:user-settings")
        else:
            messages.error(request, "Could not save your profile.")
    else:
        form = accounts_forms.UserPersonalInfoForm(instance=request.user)
    ctx["form"] = form
    return TemplateResponse(request, "accounts/personal_form.html", ctx)


class PasswordSetView(AllauthPasswordSetView):
    success_url = reverse_lazy("accounts:user-settings")


password_set_view = login_required(PasswordSetView.as_view())