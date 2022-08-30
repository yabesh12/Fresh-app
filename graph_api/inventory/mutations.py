import graphene
from django.db import transaction
from graphql import GraphQLError

from graphql_jwt.decorators import login_required

from sales_executive.models import SalesExecutive, Inventory
from graph_api.inventory.input import InventoryProductStockUpdateInput
from product.models import Product
from django.utils import timezone


class CreateInventory(graphene.Mutation):
    class Arguments:
        sales_executive_id = graphene.ID(required=True)
        stock_details = graphene.List(InventoryProductStockUpdateInput, required=True)

    message = graphene.String()

    @login_required
    @transaction.atomic
    def mutate(self, info, sales_executive_id, stock_details):
        user = info.context.user
        try:
            login_sales_executive = SalesExecutive.objects.get(user=user, is_active=True)
        except SalesExecutive.DoesNotExist:
            raise GraphQLError('You are not Sales Executive!')
        try:
            sales_executive = SalesExecutive.objects.get(id=sales_executive_id, is_active=True)
        except SalesExecutive.DoesNotExist:
            raise GraphQLError('Invalid SalesExecutive!')
        if login_sales_executive.id != sales_executive.id:
            raise GraphQLError('You are not Authorized!')
        inventories_to_be_created = []
        invalid_skus = []
        for stock_detail in stock_details:
            product_sku = stock_detail.get('product_sku')
            stock = stock_detail.get('stock')
            incoming_type = stock_detail.get('incoming_type')
            try:
                product = Product.objects.get(sku=product_sku)
            except Product.DoesNotExist:
                invalid_skus.append(product_sku)
            inventories_to_be_created.append(Inventory(
                sales_executive=sales_executive,
                product=product,
                stock=stock,
                incoming_type=incoming_type,
                date_time=timezone.now()
            ))
        Inventory.objects.bulk_create(inventories_to_be_created)
        if not len(invalid_skus):
            return CreateInventory(message=f"Success")
        return CreateInventory(message=f"Invalid Product SKU's {invalid_skus}")


class InventoryMutation(graphene.ObjectType):
    create_inventory = CreateInventory.Field()
