from decimal import Decimal

from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from address.models import Address
from core.models import DateTimeModel
from group.models import PriceGroup
from shop.managers import ShopManager

REGEX_PHONE = RegexValidator(r'^(?!0|1|2|3|4|5)[0-9]{10}$', 'Invalid Mobile Number!')


class Shop(DateTimeModel, MPTTModel):
    price_group = models.ForeignKey(PriceGroup, on_delete=models.CASCADE, related_name="shop_price_group")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="shop_address")
    name = models.CharField(max_length=150)
    gst_number = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=10, validators=[REGEX_PHONE])
    wallet = models.DecimalField(decimal_places=2, max_digits=7, default=0.0,
                                 validators=[MinValueValidator(Decimal('0.00'))])
    total_credit_limit = models.DecimalField(decimal_places=2, max_digits=7, default=0.0)
    total_credit = models.DecimalField(decimal_places=2, max_digits=7, default=0.0,
                                       validators=[MaxValueValidator(Decimal('0.00'))])
    is_chain = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    objects = ShopManager()

    def __str__(self):
        return f'{self.id} - {self.name}'
