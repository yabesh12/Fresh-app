from django.contrib.auth import get_user_model
from django.db import models
from address.models import Address
from core.models import DateTimeModel
from product.models import Product
from route.models import Route
from sales_executive.managers import SalesExecutiveManager

User = get_user_model()


class SalesExecutive(DateTimeModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    permanent_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True,
                                          related_name="sales_executive_perm_address")
    temporary_address = models.ForeignKey(Address, on_delete=models.CASCADE,
                                          related_name="sales_executive_temp_address", blank=True, null=True)
    permanent_route = models.ForeignKey(Route, on_delete=models.CASCADE,
                                        related_name="permanent_route", blank=True, null=True)
    temporary_route = models.ForeignKey(Route, on_delete=models.CASCADE,
                                        related_name="temporary_route", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    custom_objects = SalesExecutiveManager()

    def __str__(self):
        return f"{self.user.username}"


IN_TYPE = (
    ("NEW", "NEW"),
    ("RETURN", "RETURN"),
)


class Inventory(DateTimeModel):
    sales_executive = models.ForeignKey(SalesExecutive, on_delete=models.CASCADE,
                                        related_name="inventory_sales_executive")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventory_product")
    stock = models.PositiveIntegerField()
    date_time = models.DateTimeField()
    incoming_type = models.CharField(max_length=150, choices=IN_TYPE, default="NEW")

    def __str__(self):
        return f"{self.id} - {self.sales_executive.user.username} - {self.product.name} - {self.stock} - {self.date_time} " \
               f"- {self.incoming_type}"
