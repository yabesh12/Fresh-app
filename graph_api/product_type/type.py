from graphene import Node
from graphene_django import DjangoObjectType

from product.models import ProductType


class ProductTypeType(DjangoObjectType):
    """GraphQL Type for ProductType (Product's GraphQL Type named as "RealProductType")
    """
    class Meta:
        model = ProductType
        field = '__all__'
        interfaces = (Node,)

