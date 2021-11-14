from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("settings/", views.user_settings, name="user-settings"),
    path("update/", views.user_update, name="user-update"),
    path("standard-access/", views.standard_access, name="standard-access"),
    path("pro-access/", views.pro_access, name="pro-access"),
]
