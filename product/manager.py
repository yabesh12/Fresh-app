from django.db.models import manager, OuterRef, Subquery, Case, When, F

from group.models import GroupBasedPrice


class ProductShopCustomManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_selling_price_by_group(self, group):
        group_obj_subquery = GroupBasedPrice.objects.annotate(
            sell_price=Case(
                When(
                    discount_selling_price__isnull=False,
                    then=F('discount_selling_price')
                ),
                default=F('selling_price'),
            )
        ).filter(
            price_group=group,
            product_id=OuterRef('id')

        )
        products_objs = self.get_queryset().annotate(
            group_price=Subquery(group_obj_subquery.values('sell_price')[:1])
        ).annotate(
            sell_price=Case(
                When(group_price__isnull=False, then=F('group_price')),
                default=F('selling_price'),
            )
        )
        return products_objs
