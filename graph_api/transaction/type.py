from graphene_django import DjangoObjectType
from transaction.models import Transaction


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = "__all__"
