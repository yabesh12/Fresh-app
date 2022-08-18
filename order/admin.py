from django.contrib import admin

# Register your models here.
from order.models import Order, OrderItem
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemResource(resources.ModelResource):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderResourceAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    list_display = ("id", "status", "total", "is_paid")


class OrderItemResourceAdmin(ImportExportModelAdmin):
    resource_class = OrderItemResource
    list_display = ("id", "order", "product", "quantity", 'price', 'total')
    readonly_fields = ('total',)


admin.site.register(Order, OrderResourceAdmin)
admin.site.register(OrderItem, OrderItemResourceAdmin)
