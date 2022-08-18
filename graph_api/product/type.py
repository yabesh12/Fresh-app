from graphene import Node
from graphene_django import DjangoObjectType

from product.models import Product


class RealProductType(DjangoObjectType):  # Real Product Type
    class Meta:
        model = Product
        fields = '__all__'
        interfaces = (Node,)
