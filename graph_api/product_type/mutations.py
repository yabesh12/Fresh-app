import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graph_api.accounts.decorators import manager_only, admin_only
from graph_api.product_type.type import ProductTypeType
from product.models import ProductType


class CreateProductType(graphene.Mutation):
    """Create New ProductType
    """

    class Arguments:
        title = graphene.String(required=True)
        unit = graphene.String(required=True)
        tax = graphene.Decimal(required=True)
        is_credit_available = graphene.Boolean(required=True)
        is_active = graphene.Boolean(required=True)
        parent_id = graphene.ID()

    product_type = graphene.Field(ProductTypeType)

    @login_required
    @manager_only
    def mutate(self, info, title, unit, tax, is_credit_available, is_active, parent_id=None):
        parent = parent_id
        if parent:
            try:
                parent = ProductType.objects.get(id=parent_id)
            except ProductType.DoesNotExist:
                raise GraphQLError(f'Invalid Parent Product!')
        product_type, created = ProductType.objects.get_or_create(
            title=title,
            unit=unit,
            tax=tax,
            is_credit_available=is_credit_available,
            is_active=is_active,
            parent=parent
        )
        return CreateProductType(product_type=product_type)


class UpdateProductType(graphene.Mutation):
    """Updates the Existing ProductType by taking ID as Input
    """

    class Arguments:
        product_type_id = graphene.ID(required=True)
        title = graphene.String()
        unit = graphene.String()
        tax = graphene.Decimal()
        is_credit_available = graphene.Boolean()
        is_active = graphene.Boolean()
        parent_id = graphene.ID()

    product_type = graphene.Field(ProductTypeType)

    @login_required
    @manager_only
    def mutate(self, info, product_type_id, **kwargs):
        try:
            product_type = ProductType.objects.get(id=product_type_id)
        except ProductType.DoesNotExist:
            raise GraphQLError(f'Invalid ProductType!')
        if title := kwargs.get('title'):
            product_type.title = title
        if tax := kwargs.get('tax'):
            product_type.tax = tax
        if unit := kwargs.get('unit'):
            product_type.unit = unit
        if parent := kwargs.get('parent_id'):
            try:
                parent = ProductType.objects.get(id=parent)
            except ProductType.DoesNotExist:
                raise GraphQLError(f'Invalid Parent ProductType!')
            product_type.parent = parent
        active_status = kwargs.get('is_active')
        if active_status is not None and product_type.is_active != active_status:
            product_type.is_active = active_status
        credit_status = kwargs.get('is_credit_available')
        if credit_status is not None and product_type.is_credit_available != credit_status:
            product_type.is_credit_available = credit_status
        product_type.save()
        return UpdateProductType(product_type=product_type)


class DeleteProductType(graphene.Mutation):
    """Deletes the productTypes
    Note: Taking List of Product Type ID's as List
    """

    class Arguments:
        product_type_ids = graphene.List(graphene.ID, required=True)

    message = graphene.String()

    @login_required
    @admin_only
    def mutate(self, info, product_type_ids):
        product_type_objs= ProductType.objects.get(id__in=product_type_ids).delete()
        if product_type_objs == 0:
            return DeleteProductType(message="Invalid Product Type!")
        return DeleteProductType(message='ProductTypes Deleted Successfully.')


class ProductTypeMutation(graphene.ObjectType):
    create_product_type = CreateProductType.Field()
    update_product_type = UpdateProductType.Field()
    delete_product_type = DeleteProductType.Field()
