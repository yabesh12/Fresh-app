from django.db.models import manager


class RouteManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False, is_active=True).order_by('-created_at')
