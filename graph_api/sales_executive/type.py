from graphene_django import DjangoObjectType
from sales_executive.models import SalesExecutive
from graphene import Node


class SalesExecutiveType(DjangoObjectType):
    class Meta:
        model = SalesExecutive
        field = '__all__'
        interfaces = (Node,)
