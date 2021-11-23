from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from my_awesome_project.accounts.models import TrialRecord, User, UserProfile


class UserProfileInline(admin.TabularInline):
    model = UserProfile


class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]


admin.site.register(User, UserAdmin)
admin.site.register(TrialRecord)
