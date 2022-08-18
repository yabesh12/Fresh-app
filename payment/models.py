from django.db import models

from core.models import DateTimeModel
from order.models import Order
from sales_executive.models import SalesExecutive
from shop.models import Shop

PAYMENT_TYPE_CHOICES = (
    ('CREDIT', 'CREDIT'),
    ('DEBIT', 'DEBIT'),
)


class Payment(DateTimeModel):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    sales_executive = models.ForeignKey(SalesExecutive, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name="payments")
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES, default='DEBIT')
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    remarks = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.shop} - {self.order} - {self.payment_type}'
