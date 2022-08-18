from django.contrib import admin

# Register your models here.
from payment.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "payment_type", "shop", "sales_executive")


admin.site.register(Payment, PaymentAdmin)
