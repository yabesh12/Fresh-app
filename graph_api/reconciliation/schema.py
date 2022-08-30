import graphene
from graphql import GraphQLError

from graph_api.reconciliation.type import ReconciliationType
from reconciliation.models import Reconciliation
from graphql_jwt.decorators import login_required

from sales_executive.models import SalesExecutive


class ReconciliationQuery(graphene.ObjectType):
    get_reconciliation_by_id = graphene.Field(ReconciliationType, reconciliation_id=graphene.ID())
    all_reconciliations = graphene.List(ReconciliationType)

    @login_required
    def resolve_get_reconciliation_by_id(self, info, reconciliation_id):
        user = info.context.user
        if user.is_manager:
            try:
                reconciliation = Reconciliation.objects.get(id=reconciliation_id)
            except Reconciliation.DoesNotExist:
                raise GraphQLError('Invalid Reconciliation!')
            return reconciliation
        try:
            reconciliation = Reconciliation.objects.get(id=reconciliation_id, sales_executive__user=user)
        except Reconciliation.DoesNotExist:
            raise GraphQLError('Invalid Reconciliation!')
        return reconciliation

    @login_required
    def resolve_all_reconciliations(self, info):
        user = info.context.user
        if user.is_manager:
            return Reconciliation.objects.all().order_by('-created_at')
        return Reconciliation.objects.filter(sales_executive__user=user).order_by('-created_at')



