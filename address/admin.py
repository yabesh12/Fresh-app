from django.contrib import admin

# Register your models here.
from address.models import Address
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'address_line1', 'address_lin2', 'city', 'pincode', 'is')
admin.site.register(Address)