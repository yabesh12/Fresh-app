import graphene
from graphql import GraphQLError
from .type import TransactionType
from transaction.models import Transaction


class TransactionQuery(graphene.ObjectType):
    get_transaction_by_id = graphene.Field(TransactionType, transaction_id=graphene.ID())
    all_transactions = graphene.List(TransactionType)

    def resolve_get_transaction_by_id(self, info, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            raise GraphQLError('Invalid Transaction!')
        return transaction

    def resolve_all_transaction(self, info):
        return Transaction.objects.all()