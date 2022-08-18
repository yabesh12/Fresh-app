import timeit

import graphene
from graphql import GraphQLError
from django.core.cache import cache
from graphql_jwt.decorators import login_required

from graph_api.accounts.decorators import manager_only
from graph_api.product.type import RealProductType
from product.models import Product


class ProductQuery(graphene.ObjectType):
    """
    List all active products
    Get active product by ID
    """
    product_by_sku = graphene.Field(RealProductType, product_sku=graphene.String())
    all_products = graphene.List(RealProductType)

    @login_required
    def resolve_product_by_id(self, info, product_sku):
        if info.context.user.is_manager:
            try:
                product = Product.objects.get(sku=product_sku)
            except Product.DoesNotExist:
                raise GraphQLError(f'Invalid Product {product_sku}.')
            return product

        try:
            product = Product.objects.get(sku=product_sku, is_active=True)
        except Product.DoesNotExist:
            raise GraphQLError(f'Invalid Product{product_sku}.')
        return product

    @login_required
    def resolve_all_products(self, info):
        return Product.objects.filter(is_active=True, is_deleted=False).order_by('-created_at')
