from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("settings/", views.user_settings, name="user-settings"),
    path("update/", views.user_update, name="user-update"),
]
