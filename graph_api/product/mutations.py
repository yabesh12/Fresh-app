import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graph_api.accounts.decorators import manager_only, admin_only
from graph_api.product.type import RealProductType
from product.models import Product, Category, ProductType


class CreateProduct(graphene.Mutation):
    """Creates New Product
    """

    class Arguments:
        name = graphene.String(required=True)
        sku = graphene.String(required=True)
        base_price = graphene.Decimal(required=True)
        selling_price = graphene.Decimal(required=True)
        mrp_price = graphene.Decimal(required=True)
        unit = graphene.String(required=True)
        weight = graphene.String(required=True)
        is_active = graphene.Boolean(required=True)
        self_life = graphene.Int(required=True)
        parent_id = graphene.ID()
        category_id = graphene.ID()
        product_type_id = graphene.ID()

    product = graphene.Field(RealProductType)

    @login_required
    @manager_only
    def mutate(self, info, name, sku, base_price, selling_price, mrp_price, unit, weight, is_active,
               self_life, parent_id=None, category_id=None, product_type_id=None):
        product_obj = Product.objects.filter(sku=sku)
        if product_obj.exists():
            raise GraphQLError("Product Already Exists. Please Change SKU and Try Again!")
        parent = parent_id
        category = category_id
        product_type = product_type_id
        if parent:
            try:
                parent = Product.objects.get(id=parent_id)
            except Product.DoesNotExist:
                raise GraphQLError('Invalid Parent Product!')
        if category:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                raise GraphQLError('Invalid Category!')
        if product_type:
            try:
                product_type = ProductType.objects.get(id=product_type_id)
            except ProductType.DoesNotExist:
                raise GraphQLError('Invalid ProductType!')
        product_obj, created = Product.objects.get_or_create(
            name=name,
            sku=sku,
            base_price=base_price,
            selling_price=selling_price,
            mrp_price=mrp_price,
            unit=unit,
            weight=weight,
            is_active=is_active,
            self_life=self_life,
            parent=parent,
            category=category,
            product_type=product_type
        )
        product_obj.save()
        return CreateProduct(product=product_obj)


class UpdateProduct(graphene.Mutation):
    """Updates the Existing Product
    """

    class Arguments:
        product_id = graphene.ID(required=True)
        name = graphene.String()
        sku = graphene.String()
        base_price = graphene.Decimal()
        selling_price = graphene.Decimal()
        mrp_price = graphene.Decimal()
        unit = graphene.String()
        weight = graphene.String()
        is_active = graphene.Boolean()
        self_life = graphene.String()
        parent_id = graphene.ID()
        category_id = graphene.ID()
        product_type_id = graphene.ID()

    product = graphene.Field(RealProductType)

    @login_required
    @manager_only
    def mutate(self, info, product_id, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise GraphQLError(f'Invalid Product!')
        if sku := kwargs.get('sku'):
            if Product.objects.filter(sku=sku).exists():
                raise GraphQLError('Product SKU Already Exists. Please use different SKU!')
            product.sku = sku
        if name := kwargs.get('name'):
            product.name = name
        if base_price := kwargs.get('base_price'):
            product.base_price = base_price
        if selling_price := kwargs.get('selling_price'):
            product.selling_price = selling_price
        if mrp_price := kwargs.get('mrp_price'):
            product.mrp_price = mrp_price
        if unit := kwargs.get('unit'):
            product.unit = unit
        if weight := kwargs.get('weight'):
            product.weight = weight
        if self_life := kwargs.get('self_life'):
            product.self_life = self_life
        if parent := kwargs.get('parent_id'):
            try:
                parent_product = Product.objects.get(id=parent)
                product.parent = parent_product
            except Product.DoesNotExist:
                raise GraphQLError('Invalid Parent Product!')
        if category := kwargs.get('category_id'):
            try:
                category = Category.objects.get(id=category)
                product.category = category
            except Category.DoesNotExist:
                raise GraphQLError(f'Invalid Category!')
        if product_type := kwargs.get('product_type_id'):
            try:
                product_type = ProductType.objects.get(id=product_type)
                product.product_type = product_type
            except ProductType.DoesNotExist:
                raise GraphQLError(f'Invalid ProductType!')
        active_status = kwargs.get('is_active')
        if active_status is not None and product.is_active != active_status:
            product.is_active = active_status
        product.save()
        return UpdateProduct(product=product)


class DeleteProduct(graphene.Mutation):
    """Deletes products
    Note: Taking an input as List of product ID's
    """

    class Arguments:
        product_ids = graphene.List(graphene.ID, required=True)

    message = graphene.String()

    @login_required
    @admin_only
    def mutate(self, info, product_ids):
        product_objs = Product.objects.filter(id__in=product_ids).update(is_deleted=True)
        if product_objs == 0:
            return DeleteProduct(message="Invalid Product!")

        return DeleteProduct(message='Products Deleted Successfully.')


class ProductMutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()
