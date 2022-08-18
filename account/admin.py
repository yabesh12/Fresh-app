from django.contrib import admin
from account.models import CustomUser

admin.site.register(CustomUser)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "username", "mobile_number")