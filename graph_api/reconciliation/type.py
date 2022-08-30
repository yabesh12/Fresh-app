from graphene_django import DjangoObjectType

from reconciliation.models import Reconciliation, ReconciliationItem


class ReconciliationType(DjangoObjectType):
    class Meta:
        model = Reconciliation
        fields = '__all__'


class ReconciliationItemType(DjangoObjectType):
    class Meta:
        model = ReconciliationItem
        fields = '__all__'
