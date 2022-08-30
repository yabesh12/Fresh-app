from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from core.models import DateTimeModel

PINCODE_VALIDATOR = RegexValidator(r'^[1-9][0-9]{5}$', 'Invalid Pincode!')


class Address(DateTimeModel):
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=8, validators=[PINCODE_VALIDATOR])
    country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}"
