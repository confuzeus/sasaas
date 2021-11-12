from django.contrib import admin

from . import models as accounts_models

admin.site.register(accounts_models.MembershipType)
admin.site.register(accounts_models.Membership)
