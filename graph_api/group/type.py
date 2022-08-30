from graphene import Node
from graphene_django import DjangoObjectType

from group.models import PriceGroup, GroupBasedPrice


class PriceGroupType(DjangoObjectType):
    class Meta:
        model = PriceGroup
        field = '__all__'
        interfaces = (Node,)


class GroupBasedPriceType(DjangoObjectType):
    class Meta:
        model = GroupBasedPrice
        field = '__all__'
        interfaces = (Node,)
