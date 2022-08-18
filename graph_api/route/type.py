from graphene import Node
from graphene_django import DjangoObjectType

from route.models import Route


class RouteType(DjangoObjectType):
    class Meta:
        model = Route
        field = '__all__'
        interfaces = (Node,)
