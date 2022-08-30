from django.db import models

# Create your models here.
from core.models import DateTimeModel
from product.models import Product
from sales_executive.models import SalesExecutive
from shop.models import Shop

ORDER_STATUS = (
    ("Pending", "Pending"),
    ("Completed", "Completed"),
    ("Failed", "Failed"),
)


class Order(DateTimeModel):
    status = models.CharField(max_length=150, choices=ORDER_STATUS, default="Pending")
    billed_to = models.ForeignKey(Shop, on_delete=models.PROTECT, related_name="orders")
    billed_by = models.ForeignKey(SalesExecutive, on_delete=models.SET_NULL, related_name="orders", null=True,
                                  blank=True)
    bill_date = models.DateField(null=True, blank=True)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    paid_date = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    out_standing_credit = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.id} - {self.billed_by} - {self.billed_to}"

    @property
    def get_total_amount_or_total_payable(self):
        total = 0
        for order_item in self.order_items.all():
            total += float(order_item.get_total())
        if total != self.total:
            self.total = total
            self.save()
        if self.discount:
            total -= float(self.discount)
        if self.out_standing_credit:
            total += float(self.out_standing_credit)
        return total


class OrderItem(DateTimeModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True, null=True)
    price = models.DecimalField(max_length=100, default=0, max_digits=7, decimal_places=2)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    # need to add tax percentage along with it tax may be changed in future so we need to add tax percentage in this

    def __str__(self):
        return f"{self.id} - {self.order}"

    def get_total(self):
        return round(float(self.price) * float(self.quantity))

    def save(self, *args, **kwargs):
        self.total = self.get_total()
        super().save(*args, **kwargs)
