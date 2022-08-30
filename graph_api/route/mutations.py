import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from graph_api.accounts.decorators import manager_only, admin_only
from route.models import Route


class CreateUpdateRoute(graphene.Mutation):
    """
    Only Manager can create or update the Route
    """

    class Arguments:
        name = graphene.String(required=True)
        starting_point = graphene.String(required=True)
        ending_point = graphene.String(required=True)
        is_active = graphene.Boolean()
        description = graphene.String()

    status = graphene.String()
    message = graphene.String()

    @login_required
    @manager_only
    def mutate(self, info, name, starting_point, ending_point, **kwargs):
        description = kwargs.get('description')
        is_active = kwargs.get('is_active', True)
        try:
            route_obj, created = Route.objects.update_or_create(name=name,
                                                                defaults={'starting_point': starting_point,
                                                                          'ending_point': ending_point,
                                                                          'is_active': is_active,
                                                                          'description': description})
            if not created:
                msg = f"Route {route_obj.name} updated successfully."
            else:
                msg = f"New Route {route_obj.name} created successfully."
        except Exception as e:
            return e

        return CreateUpdateRoute(status="Ok", message=msg)


class DeleteRoute(graphene.Mutation):
    """
    Admin can
    -> Remove the sales executive if sales executive exists
    """

    class Arguments:
        route_id = graphene.ID(required=True)

    status = graphene.String()
    message = graphene.String()

    @login_required
    @admin_only
    def mutate(self, info, route_id, **kwargs):

        try:
            route_obj = Route.objects.get(id=route_id)
            route_obj.is_deleted = True
            route_obj.save(update_fields=['is_deleted'])

        except Route.DoesNotExist:
            raise GraphQLError('Invalid Route!')

        return DeleteRoute(status="Ok", message="Successfully deleted the route")


class RouteMutation(graphene.ObjectType):
    create_update_route = CreateUpdateRoute.Field()
    delete_route = DeleteRoute.Field()
