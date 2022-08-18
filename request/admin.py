from django.contrib import admin

# Register your models here.
from request.models import Request, RequestItem
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class RequestResource(resources.ModelResource):
    class Meta:
        model = Request
        fields = "__all__"


class RequestItemResource(resources.ModelResource):
    class Meta:
        model = RequestItem
        fields = "__all__"


class RequestResourceAdmin(ImportExportModelAdmin):
    resource_class = RequestResource
    list_display = ("id", "sales_executive", "shop", "due_date")


class RequestItemResourceAdmin(ImportExportModelAdmin):
    resource_class = RequestItemResource
    list_display = ("id", "request", "product", "quantity")


admin.site.register(Request, RequestResourceAdmin)
admin.site.register(RequestItem, RequestItemResourceAdmin)
