from django.db import models

from core.models import DateTimeModel


class Route(DateTimeModel):
    name = models.CharField(max_length=200, unique=True)
    starting_point = models.CharField(max_length=100)
    ending_point = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id} - {self.name}'
