from django.contrib import admin

# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from shop.models import Shop


class ShopResource(resources.ModelResource):
    class Meta:
        model = Shop
        fields = "__all__"


class ShopResourceAdmin(ImportExportModelAdmin):
    resource_class = ShopResource
    list_display = ("id", "name", "price_group",)


admin.site.register(Shop, ShopResourceAdmin)
