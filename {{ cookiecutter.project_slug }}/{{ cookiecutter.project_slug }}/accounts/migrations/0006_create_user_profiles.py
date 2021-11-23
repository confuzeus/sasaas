# Generated by Django 3.2.9 on 2021-11-23 05:43

from django.db import migrations
from django.conf import settings


def create_user_profiles(apps, schema_editor):
    user_app_label, user_model = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(user_app_label, user_model)
    UserProfile = apps.get_model("accounts", "UserProfile")
    for user in User.objects.all():
        profile = UserProfile(user=user, country=None)
        profile.save()


def delete_user_profiles(apps, schema_editor):
    user_app_label, user_model = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(user_app_label, user_model)
    for user in User.objects.all():
        user.profile.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_userprofile"),
    ]

    operations = [migrations.RunPython(create_user_profiles, delete_user_profiles)]
