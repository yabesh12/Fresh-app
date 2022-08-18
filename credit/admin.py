from django.contrib import admin

# Register your models here.
from credit.models import Credit, CreditLimit


class CreditAdmin(admin.ModelAdmin):
    list_display = ("id", "shop", "category", "amount",)


class CreditLimitAdmin(admin.ModelAdmin):
    list_display = ("id", "shop", "category",)


admin.site.register(Credit, CreditAdmin)
admin.site.register(CreditLimit, CreditLimitAdmin)
