from graphene import Node
from graphene_django import DjangoObjectType

from sales_executive.models import Inventory


class InventoryType(DjangoObjectType):
    class Meta:
        model = Inventory
        fields = '__all__'
        interfaces = (Node,)
