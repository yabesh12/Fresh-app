import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from graph_api.category.type import CategoryType
from product.models import Category


class CategoryQuery(graphene.ObjectType):
    """Lists All active Categories
    Gets active Category by ID
    """
    category_by_id = graphene.Field(CategoryType, category_id=graphene.ID())
    all_categories = graphene.List(CategoryType)

    @login_required
    def resolve_category_by_id(self, info, category_id):
        if info.context.user.is_manager:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                raise GraphQLError(f'Invalid Category!')
            return category
        try:
            category = Category.objects.get(id=category_id, is_active=True)
        except Category.DoesNotExist:
            raise GraphQLError(f'Invalid Category!')
        return category

    @login_required
    def resolve_all_categories(self, info):
        return Category.objects.filter(is_active=True, is_deleted=False).order_by('-created_at')

