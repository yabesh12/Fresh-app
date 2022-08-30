from django.db import models
from core.models import DateTimeModel
from product.models import Category
from shop.models import Shop


class Credit(DateTimeModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="credit_category")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="credit_shop")
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        unique_together = ('shop', 'category',)

    def __str__(self):
        return f"{self.id} - {self.shop}"


class CreditLimit(DateTimeModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="credit_limit_category")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="credit_limit_shop")
    percentage = models.PositiveIntegerField()

    class Meta:
        unique_together = ('shop', 'category',)

    def __str__(self):
        return f"{self.id} - Category({self.category}) - Shop({self.shop})"

    @property
    def credit_limit_amount_available(self):
        try:
            if not self.category.product_type.is_credit_available:
                return 0
            shop_max_credit_limit = self.shop.total_credit_limit
            percentage = self.percentage
            credit_amount_max_per_category = int(shop_max_credit_limit) * (percentage / 100)
            return credit_amount_max_per_category
        except Exception as e:
            print(e)
            return 0
