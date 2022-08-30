import graphene
from graphql_jwt.decorators import login_required

from graph_api.accounts.decorators import manager_only
from graph_api.group.type import PriceGroupType
from group.models import PriceGroup


class PriceGroupQuery(graphene.ObjectType):
    price_groups = graphene.List(PriceGroupType)

    # @login_required
    # @manager_only
    def resolve_price_groups(self, info):
        return PriceGroup.custom_objects.all()
