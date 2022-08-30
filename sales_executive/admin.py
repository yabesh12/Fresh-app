from django.contrib import admin

# Register your models here.
from sales_executive.models import SalesExecutive, Inventory
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class SalesExecutiveResource(resources.ModelResource):
    class Meta:
        model = SalesExecutive
        fields = "__all__"


class InventoryResource(resources.ModelResource):
    class Meta:
        model = Inventory
        fields = "__all__"


class SalesExecutiveResourceAdmin(ImportExportModelAdmin):
    resource_class = SalesExecutiveResource
    list_display = ("id", "user", "is_active", "is_deleted",)

class InventoryResourceAdmin(ImportExportModelAdmin):
    resource_class = InventoryResource


admin.site.register(SalesExecutive, SalesExecutiveResourceAdmin)
admin.site.register(Inventory)
