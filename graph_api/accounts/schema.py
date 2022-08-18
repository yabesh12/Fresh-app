import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required

from graph_api.accounts.decorators import manager_only
from graph_api.accounts.type import UserType

User = get_user_model()


class GetAllUsers(graphene.ObjectType):
    get_all_users = graphene.List(UserType)

    @login_required
    @manager_only
    def resolve_get_all_users(self, info, **kwargs):
        return User.objects.filter(is_active=True).order_by('-date_joined')
