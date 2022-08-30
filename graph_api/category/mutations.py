import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graph_api.accounts.decorators import manager_only, admin_only
from graph_api.category.type import CategoryType
from product.models import Category, ProductType


class CreateCategory(graphene.Mutation):
    """Creates New Category
    """

    class Arguments:
        name = graphene.String(required=True)
        is_active = graphene.Boolean(required=True)
        parent_id = graphene.ID()
        product_type_id = graphene.ID()

    category = graphene.Field(CategoryType)

    @login_required
    @manager_only
    def mutate(self, info, name, is_active, parent_id=None, product_type_id=None):
        if Category.objects.filter(name=name).exists():
            raise GraphQLError(f'Category {name} already Exist!')
        parent_category = parent_id
        product_type = product_type_id
        if parent_category:
            try:
                parent_category = Category.objects.get(id=parent_id)
            except Category.DoesNotExist:
                raise GraphQLError("Invalid Parent Category!")
        if product_type:
            try:
                product_type = ProductType.objects.get(id=product_type)
            except Category.DoesNotExist:
                raise GraphQLError('Invalid ProductType!')
        category_obj, created = Category.objects.get_or_create(
            name=name,
            is_active=is_active,
            parent=parent_category,
            product_type=product_type,
        )
        return CreateCategory(category=category_obj)


class UpdateCategory(graphene.Mutation):
    """Updates Existing Category
    """

    class Arguments:
        category_id = graphene.ID(required=True)
        name = graphene.String()
        is_active = graphene.Boolean()
        parent_id = graphene.ID()
        product_type_id = graphene.ID()

    category = graphene.Field(CategoryType)

    @login_required
    @manager_only
    def mutate(self, info, category_id, **kwargs):
        if not bool(kwargs):
            raise GraphQLError('Nothing to Update!')
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise GraphQLError(f'Invalid Category!')
        if name := kwargs.get('name'):
            category.name = name
        if parent_id := kwargs.get('parent_id'):
            try:
                parent_category = Category.objects.get(id=parent_id)
            except Category.DoesNotExist:
                raise GraphQLError(f'Invalid Parent Category!')
            category.parent = parent_category
        if product_type_id := kwargs.get('product_type_id'):
            try:
                product_type = ProductType.objects.get(id=product_type_id)
            except ProductType.DoesNotExist:
                raise GraphQLError(f'Invalid ProductType!')
            category.product_type = product_type
        active_status = kwargs.get('is_active')
        if active_status is not None and category.is_active != active_status:
            category.is_active = active_status
        category.save()
        return UpdateCategory(category=category)


class DeleteCategory(graphene.Mutation):
    """Deletes Categories
    Note: Taking input as List of Category ID's to be deleted
    """

    class Arguments:
        category_ids = graphene.List(graphene.ID, required=True)

    message = graphene.String()

    @login_required
    @admin_only
    def mutate(self, info, category_ids):
        category_objs = Category.objects.filter(id__in=category_ids).delete()
        if category_objs == 0:
            return DeleteCategory(message="Invalid Category!")
        return DeleteCategory(message='Category(s) Deleted Successfully!')


class CategoryMutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
