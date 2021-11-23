from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("settings/", views.user_settings, name="user-settings"),
    path("update/", views.user_update, name="user-update"),
    path("standard-access/", views.standard_access, name="standard-access"),
    path("pro-access/", views.pro_access, name="pro-access"),
    path("upgrade/", views.upgrade_membership, name="upgrade"),
    path("trial/<str:membership_code>/", views.activate_trial, name="activate_trial"),
    path("wallet/", views.wallet_view, name="wallet"),
]
