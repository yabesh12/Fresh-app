import graphene
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from graph_api.order.type import OrderNode
from order.models import Order


class OrderQuery(graphene.ObjectType):
    all_orders = graphene.List(OrderNode)
    order_by_id = graphene.Field(OrderNode, id=graphene.ID(required=True))
    orders_by_shop_id = graphene.Field(OrderNode, shop_id=graphene.ID(required=True))

    @login_required
    def resolve_all_orders(self, info):
        user = info.context.user
        if user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(billed_by__user=user)

    @login_required
    def resolve_order_by_id(self, info, id):
        user = info.context.user
        id = from_global_id(id)[1]
        if user.is_superuser:
            return Order.objects.filter(id=id).first()
        return Order.objects.filter(billed_by__user=user, id=id).first()

    @login_required
    def resolve_orders_by_shop_id(self, info, shop_id):
        user = info.context.user
        shop_id = from_global_id(shop_id)[1]
        if user.is_superuser:
            return Order.objects.filter(billed_to__id=shop_id)
        return Order.objects.filter(billed_by__user=user, billed_to__id=shop_id)
