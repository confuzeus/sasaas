from allauth.account.views import PasswordSetView as AllauthPasswordSetView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from . import forms as accounts_forms
from .forms import MembershipUpgradeForm, TrialRecordForm, UserProfileForm
from ..core.decorators import group_required
from ..core.utils.urls import redirect_next_or_default


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


@login_required
def upgrade_membership(request):
    form = None
    ctx = {}
    if request.method == "POST":
        form = MembershipUpgradeForm(request.POST, user=request.user)

        if form.is_valid():
            pass

    if not form:
        form = MembershipUpgradeForm(user=request.user)

    ctx.update({"upgrade_form": form})
    return TemplateResponse(request, "accounts/upgrade.html", ctx)


@login_required
def activate_trial(request, membership_code):
    if request.method == "POST":
        form = TrialRecordForm(
            {"user": request.user, "membership_code": membership_code}
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                _(
                    f"Your {settings.MEMBERSHIP_GROUPS[membership_code]['name']} membership trial has been activated."
                ),
            )
            return redirect(settings.LOGIN_REDIRECT_URL)

    return redirect(settings.UPGRADE_URL)


@login_required
def wallet_view(request):
    ctx = {}
    payment_success = request.GET.get("success")
    if payment_success:
        messages.success(
            request,
            "Your payment has been received. Please wait for your wallet to update.",
        )
        return redirect("accounts:wallet")
    return TemplateResponse(request, "accounts/wallet.html", ctx)


@login_required
def update_user_profile(request):
    ctx = {}
    form = None
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect_next_or_default(
                path=request.path, default="accounts:user-settings"
            )

    if not form:
        form = UserProfileForm(instance=request.user.profile)

    ctx["form"] = form
    return TemplateResponse(request, "accounts/update_profile.html", ctx)


# Some dummy views to illustrate memberships


@group_required("1")
def standard_access(request):
    return HttpResponse("OK")


@group_required("2")
def pro_access(request):
    return HttpResponse("OK")
