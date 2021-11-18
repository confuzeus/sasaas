from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from my_awesome_project.accounts.models import TrialRecord, User

admin.site.register(TrialRecord)
admin.site.register(User, UserAdmin)
