import graphene
from graphene_django import DjangoObjectType

from order.models import Order, OrderItem


class OrderNode(DjangoObjectType):
    """
    GraphQL Type for Order
    """

    class Meta:
        model = Order
        fields = '__all__'
        # filter_fields = {
        #     'id': ['exact'],
        #     'invoice_number': ['exact'],
        #     'shop_id': ['exact'],
        # }
        interfaces = (graphene.relay.Node,)


class OrderItemNode(DjangoObjectType):
    """
    GraphQL Type for OrderItem
    """

    class Meta:
        model = OrderItem
        fields = '__all__'
        # filter_fields = {
        #     'id': ['exact'],
        #     'order_id': ['exact']
        # }
        interfaces = (graphene.relay.Node,)


class CreditAvailabilityResponseType(graphene.ObjectType):
    """
    GraphQL Type for CreditAvailabilityResponse
    """
    category_id = graphene.Int()
    category_name = graphene.String()
    credit_limit = graphene.Float()
    credit_amount = graphene.Float()
    credit_available = graphene.Int()
    order_amount = graphene.Float()
    is_credit_available = graphene.Boolean()
    status = graphene.String()
