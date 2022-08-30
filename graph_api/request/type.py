from graphene import Node
from graphene_django import DjangoObjectType

from request.models import Request


class RequestType(DjangoObjectType):
    class Meta:
        model = Request
        fields = "__all__"
        interfaces = (Node,)