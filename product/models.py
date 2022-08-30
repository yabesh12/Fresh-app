from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from core.models import DateTimeModel
from product.manager import ProductShopCustomManager

UNIT_TYPES = (
    ("PENDING", "PENDING"),
    ("KG", "KG"),
    ("GRAM", "GRAM"),
    ("DOZEN", "DOZEN"),
    ("PACKET", "PACKET"),
    ("CASE", "CASE"),
)


class ProductType(DateTimeModel, MPTTModel):
    title = models.CharField(max_length=200, unique=True)
    unit = models.CharField(max_length=150, choices=UNIT_TYPES, default="PENDING")
    tax = models.DecimalField(max_digits=7, decimal_places=2)
    is_credit_available = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Category(DateTimeModel, MPTTModel):
    product_type = TreeForeignKey(ProductType, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='category_product_type')
    name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Product(DateTimeModel, MPTTModel):
    product_type = TreeForeignKey(ProductType, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='product_type')
    category = TreeForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='product_category')
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=200, unique=True)
    shelf_life = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=7, decimal_places=2)
    selling_price = models.DecimalField(max_digits=7, decimal_places=2)
    mrp_price = models.DecimalField(max_digits=7, decimal_places=2)
    unit = models.CharField(max_length=150, choices=UNIT_TYPES, default="PENDING")
    weight = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    custom_shop_manager = ProductShopCustomManager()

    def __str__(self):
        return f"{self.sku}"
