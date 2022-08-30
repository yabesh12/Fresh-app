from graphql import GraphQLError

from reconciliation.models import Reconciliation, ReconciliationItem
from sales_executive.models import SalesExecutive


def update_authorization(reconciliation_id, kwargs, user):

