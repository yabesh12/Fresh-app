from django.contrib.auth import get_user_model
from graphene import Node
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude_fields = ('password',)
        interfaces = (Node,)
