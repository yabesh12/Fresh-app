import graphene
from graphql_jwt.decorators import login_required
from graph_api.accounts.decorators import manager_only
from sales_executive.models import SalesExecutive
from graph_api.sales_executive.type import SalesExecutiveType


class SalesExecutiveQuery(graphene.ObjectType):
    all_sales_executives = graphene.List(SalesExecutiveType)

    @login_required
    @manager_only
    def resolve_all_sales_executives(root, info):
        return SalesExecutive.custom_objects.all()
