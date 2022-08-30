import graphene
from graphql_jwt.decorators import login_required

from graph_api.shop.type import ShopType
from shop.models import Shop


class ShopQuery(graphene.ObjectType):
    all_shops = graphene.List(ShopType)

    @login_required
    def resolve_all_shops(self, info):
        return Shop.objects.filter(is_active=True)