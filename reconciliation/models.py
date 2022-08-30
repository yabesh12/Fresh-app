from django.db import models

# Create your models here.
from core.models import DateTimeModel
from product.models import Product
from request.models import Request
from sales_executive.models import SalesExecutive, Inventory
from shop.models import Shop
from transaction.models import Transaction

RE_TYPE = (
    ('VOID', 'VOID'),
    ("REFUND", "REFUND"),
    ("CREDIT", "CREDIT"),
)


class Reconciliation(DateTimeModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    sales_executive = models.ForeignKey(SalesExecutive, on_delete=models.CASCADE,
                                        related_name="recon_sales_executive")
    reconciliation_type = models.CharField(max_length=200, choices=RE_TYPE, default="VOID")
    reconciliation_date = models.DateTimeField(max_length=100)

    def __str__(self):
        return f"{self.id} - {self.shop.name}"


REI_PRODUCT_TYPE = (
    ('USABLE', 'USABLE'),
    ('DAMAGE', 'DAMAGE'),
)


class ReconciliationItem(DateTimeModel):
    reconciliation_product_type = models.CharField(max_length=6, choices=REI_PRODUCT_TYPE)
    reconciliation = models.ForeignKey(Reconciliation, on_delete=models.CASCADE,
                                       related_name="related_reconciliation")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reconciliation_item_product")
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='reconciliation_item_inventory',
                                  blank=True, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="reconciliation_item_transaction",
                                    blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.reconciliation}"
