import graphene
from graphql_jwt.decorators import login_required

from graph_api.request.type import RequestType
from request.models import Request


class RequestQuery(graphene.ObjectType):
    all_requests = graphene.List(RequestType)

    @login_required
    def resolve_all_requests(self, info):
        return Request.objects.all()
