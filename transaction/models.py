from django.db import models

from core.models import DateTimeModel


TRANSACTION_TYPE = (
    ('CREDIT', 'CREDIT'),
    ('DEBIT', 'DEBIT'),
)


class Transaction(DateTimeModel):
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.id} - {self.amount} - {self.transaction_type}'



