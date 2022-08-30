import graphene
from graphql_jwt.decorators import login_required

from graph_api.route.type import RouteType
from route.models import Route


class RouteQuery(graphene.ObjectType):
    all_routes = graphene.List(RouteType)

    @login_required
    def resolve_all_routes(self, info):
        return Route.custom_objects.all()
