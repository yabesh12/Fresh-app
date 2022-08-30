from django.db import models


class RequestManager(models.Manager):
    """
    only manager can get and view all the requests those who are not deleted
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)