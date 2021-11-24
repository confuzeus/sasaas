from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path(
        "paddle/webhook/",
        views.paddle_webhook,
        name="paddle-webhook",
    )
]
