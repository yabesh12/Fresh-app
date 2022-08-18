from django.db import models
from core.models import DateTimeModel
from product.models import Product
from request.managers import RequestManager
from sales_executive.models import SalesExecutive
from shop.models import Shop

REQ_STATUS = (
    ("PENDING", "PENDING"),
    ("HOLD", "HOLD"),
    ("FAILED", "FAILED"),
    ("COMPLETED", "COMPLETED"),
)


class Request(DateTimeModel):
    sales_executive = models.ForeignKey(SalesExecutive, on_delete=models.CASCADE,
                                        related_name="request_sales_executive")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="request_shop")
    requested_date = models.DateTimeField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=100, choices=REQ_STATUS, default="PENDING")
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = RequestManager()

    def __str__(self):
        return f"{self.id} - {self.sales_executive.user.username} - {self.shop.name}"


class RequestItem(DateTimeModel):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="request_item_requests")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="request_item_products")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.id} - {self.request}"