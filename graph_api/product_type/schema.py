import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from graph_api.product_type.type import ProductTypeType
from product.models import ProductType


class ProductTypeQuery(graphene.ObjectType):
    product_type_by_id = graphene.Field(ProductTypeType, product_type_id=graphene.ID())
    all_product_types = graphene.List(ProductTypeType)

    @login_required
    def resolve_product_type_by_id(self, info, product_type_id):
        if info.context.user.is_manager:
            try:
                product_type = ProductType.objects.get(id=product_type_id)
            except ProductType.DoesNotExist:
                raise GraphQLError(f'Invalid ProductType!')
            return product_type
        try:
            product_type = ProductType.objects.get(id=product_type_id, is_active=True)
        except ProductType.DoesNotExist:
            raise GraphQLError(f'Invalid ProductType!')
        return product_type

    @login_required
    def resolve_all_product_types(self, info):
        return ProductType.objects.filter(is_active=True, is_deleted=False).order_by('-created_at')
