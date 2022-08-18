from graphene import Node
from graphene_django import DjangoObjectType
from shop.models import Shop


class ShopType(DjangoObjectType):
    class Meta:
        model = Shop
        field = '__all__'
        interfaces = (Node,)
