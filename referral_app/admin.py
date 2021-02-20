from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (Users, Referral)


@admin.register(Users)
class UsersAdmin(ImportExportModelAdmin):
    pass


@admin.register(Referral)
class ReferralAdmin(ImportExportModelAdmin):
    pass
