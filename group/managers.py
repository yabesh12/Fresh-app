from django.db.models import manager


class PriceGroupManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_deleted=False).order_by('-created_at')
