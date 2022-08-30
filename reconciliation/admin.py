from django.contrib import admin

# Register your models here.
from reconciliation.models import Reconciliation, ReconciliationItem

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ReconciliationResource(resources.ModelResource):
    class Meta:
        model = Reconciliation
        fields = "__all__"


class ReconciliationItemResource(resources.ModelResource):
    class Meta:
        model = ReconciliationItem
        fields = "__all__"


class ReconciliationResourceAdmin(ImportExportModelAdmin):
    resource_class = ReconciliationResource
    list_display = ("id", "shop", "sales_executive", "reconciliation_type", "reconciliation_date")


class ReconciliationItemResourceAdmin(ImportExportModelAdmin):
    resource_class = ReconciliationItemResource
    list_display = ("id", "reconciliation", "product", "quantity", "price")


admin.site.register(Reconciliation, ReconciliationResourceAdmin)
admin.site.register(ReconciliationItem, ReconciliationItemResourceAdmin)
