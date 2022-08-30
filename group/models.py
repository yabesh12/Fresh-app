from django.db import models

from core.models import DateTimeModel


# from product.models import Product
from group.managers import PriceGroupManager


class PriceGroup(DateTimeModel):
    name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    custom_objects = PriceGroupManager()

    def __str__(self):
        return f"{self.id} - {self.name}"


class GroupBasedPrice(DateTimeModel):
    price_group = models.ForeignKey(PriceGroup, on_delete=models.CASCADE, blank=True, null=True)
    # circular Import issue
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="group_based_product",
                                blank=True, null=True)
    selling_price = models.DecimalField(max_digits=7, decimal_places=2)
    discount_selling_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = ('price_group', 'product',)

    def __str__(self):
        return f"{self.id} - {self.price_group}"
