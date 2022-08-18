from graphene import Node
from graphene_django import DjangoObjectType

from credit.models import Credit


class CreditType(DjangoObjectType):
    class Meta:
        model = Credit
        fields = "__all__"
        interface = (Node,)