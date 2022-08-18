from django.db import models


class SalesExecutiveManager(models.Manager):
    """
    only manager can get and view all the sales executives those who are not deleted
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_deleted=False).order_by('-created_at')
