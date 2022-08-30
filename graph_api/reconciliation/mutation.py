from decimal import Decimal

import graphene
from django.db import transaction
from graphql import GraphQLError


from graph_api.reconciliation.type import ReconciliationType
from group.models import GroupBasedPrice
from product.models import Product
from transaction.models import Transaction
from reconciliation.models import Reconciliation, ReconciliationItem
from sales_executive.models import SalesExecutive, Inventory
from shop.models import Shop
from django.utils import timezone
from graphql_jwt.decorators import login_required


class CreateReconciliation(graphene.Mutation):
    class Arguments:
        reconciliation_type = graphene.String(required=True)
        reconciliation_product_type = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        product_sku = graphene.String(required=True)
        shop_id = graphene.ID(required=True)

    reconciliation = graphene.Field(ReconciliationType)

    @login_required
    @transaction.atomic
    def mutate(self, info, shop_id, product_sku, reconciliation_type,
               reconciliation_product_type, quantity):
        try:
            sales_executive = SalesExecutive.objects.get(user=info.context.user)
        except SalesExecutive.DoesNotExist:
            raise GraphQLError('Invalid SalesExecutive!')
        try:
            shop = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            raise GraphQLError('Invalid Shop!')
        try:
            product = Product.objects.get(sku=product_sku)
        except Product.DoesNotExist:
            raise GraphQLError('Invalid Product!')
        reconciliation = Reconciliation.objects.create(
            sales_executive=sales_executive,
            shop=shop,
            reconciliation_type=reconciliation_type,
            reconciliation_date=timezone.now()
        )
        try:
            group_based_price = GroupBasedPrice.objects.get(product=product)
            price = group_based_price.selling_price
        except GroupBasedPrice.DoesNotExist:
            price = product.selling_price
        new_price = quantity * price
        reconciliation_item = ReconciliationItem.objects.create(
            reconciliation_product_type=reconciliation_product_type,
            reconciliation=reconciliation,
            product=product,
            quantity=quantity,
            price=new_price
        )
        if reconciliation.reconciliation_type == "CREDIT":
            shop.wallet += reconciliation_item.price
            shop.save(update_fields=['wallet'])
            trans = Transaction.objects.create(
                transaction_type="DEBIT",
                amount=reconciliation_item.price,
            )
            reconciliation_item.transaction = trans
        if reconciliation.reconciliation_type == "REFUND":
            trans = Transaction.objects.create(
                transaction_type="DEBIT",
                amount=reconciliation_item.price
            )
            reconciliation_item.transaction = trans
        reconciliation_item.save(update_fields=['transaction'])
        if reconciliation_product_type == "USABLE":
            inventory = Inventory.objects.create(
                sales_executive=sales_executive,
                incoming_type="RETURN",
                product=product,
                stock=quantity,
                date_time=timezone.now()
            )
            reconciliation_item.inventory = inventory
        reconciliation_item.save(update_fields=['inventory'])
        return CreateReconciliation(reconciliation=reconciliation)


# class UpdateReconciliation(graphene.Mutation):
#     class Arguments:
#         reconciliation_id = graphene.ID(required=True)
#         reconciliation_type = graphene.String()
#         reconciliation_product_type = graphene.String()
#         quantity = graphene.Int()
#         product_id = graphene.ID()
#         shop_id = graphene.ID()
#
#     reconciliation = graphene.Field(ReconciliationType)
#
#     @login_required
#     @transaction.atomic
#     def mutate(self, info, reconciliation_id, **kwargs):
#         try:
#             sales_executive = SalesExecutive.objects.get(user=info.context.user)
#         except SalesExecutive.DoesNotExist:
#             raise GraphQLError('Invalid SalesExecutive!')
#         try:
#             reconciliation = Reconciliation.objects.get(id=reconciliation_id)
#         except Reconciliation.DoesNotExist:
#             raise GraphQLError('Invalid Reconciliation!')
#         if reconciliation.sales_executive.id != sales_executive.id:
#             raise GraphQLError('You are not Authorized!')
#         if not bool(kwargs):
#             raise GraphQLError('Nothing to Update!')
#         try:
#             reconciliation_item = ReconciliationItem.objects.get(reconciliation=reconciliation)
#         except ReconciliationItem.DoesNotExist:
#             raise GraphQLError("Invalid ReconciliationItem!")
#
#         # If there is reconciliation type in input
#         if reconciliation_type := kwargs.get('reconciliation_type'):
#
#             # if existing reconciliation and input reconciliation same
#             if reconciliation.reconciliation_type == "Credit" and reconciliation_type == "Credit":
#                 pass
#
#             # if existing reconciliation is credit but input reconciliation type is not credit
#             if reconciliation.reconciliation_type == "Credit" and reconciliation_type != "Credit":
#                 reconciliation.shop.wallet -= reconciliation_item.price
#
#             # if existing reconciliation type is not credit and if that changes to credit
#             # then the amount would be added to wallet
#             if reconciliation.reconciliation_type != "Credit" and reconciliation_type == "Credit":
#                 reconciliation.shop.wallet += reconciliation_item.price
#             reconciliation.reconciliation_type = reconciliation_type
#             reconciliation.save()
#             reconciliation.shop.save()
#
#         # if there is reconciliation product type
#         if reconciliation_product_type := kwargs.get('reconciliation_product_type'):
#             if reconciliation_product_type == 'Damage':
#                 reconciliation_item.inventory.pro_type = "DAMAGED"
#                 reconciliation_item.reconciliation_product_type = reconciliation_product_type
#             if reconciliation_product_type == 'Return':
#                 reconciliation_item.inventory.pro_type = "RETURN"
#                 reconciliation_item.reconciliation_product_type = reconciliation_product_type
#             reconciliation_item.save()
#             reconciliation_item.inventory.save()
#
#         if quantity := kwargs.get('quantity'):
#             if reconciliation.reconciliation_type == "Credit":
#                 reconciliation.shop.wallet -= reconciliation_item.price
#             reconciliation.shop.save()
#             try:
#                 group_based_price = GroupBasedPrice.objects.get(product=reconciliation_item.product)
#                 price = group_based_price.selling_price
#             except GroupBasedPrice.DoesNotExist:
#                 price = reconciliation_item.product.selling_price
#
#             new_price = quantity * price
#             reconciliation_item.quantity = quantity
#             reconciliation_item.price = new_price
#             reconciliation_item.inventory.stock = quantity
#             if reconciliation.reconciliation_type == "Credit":
#                 reconciliation.shop.wallet += reconciliation_item.price
#             reconciliation_item.save()
#             reconciliation_item.inventory.save()
#             reconciliation.shop.save()
#
#         if product_id := kwargs.get('product_id'):
#             try:
#                 product = Product.objects.get(id=product_id)
#             except Product.DoesNotExist:
#                 raise GraphQLError('Invalid Product!')
#             if reconciliation.reconciliation_type == "Credit":
#                 reconciliation.shop.wallet -= reconciliation_item.price
#             try:
#                 group_based_price = GroupBasedPrice.objects.get(product=product)
#                 price = group_based_price.selling_price
#             except GroupBasedPrice.DoesNotExist:
#                 price = product.selling_price
#             new_price = reconciliation_item.quantity * price
#             reconciliation_item.product = product
#             reconciliation_item.price = new_price
#             reconciliation_item.inventory.product = product
#             reconciliation_item.inventory.save()
#             if reconciliation.reconciliation_type == "Credit":
#                 reconciliation.shop.wallet += reconciliation_item.price
#             reconciliation.shop.save()
#             reconciliation_item.save()
#
#         if shop_id := kwargs.get('shop_id'):
#             try:
#                 shop = Shop.objects.get(id=shop_id)
#             except Shop.DoesNotExist:
#                 raise GraphQLError('Invalid Shop!')
#             if reconciliation.reconciliation_type == "Credit":
#                 reconciliation.shop.wallet -= reconciliation_item.price
#             reconciliation.shop.save()
#             reconciliation.shop = shop
#             reconciliation.save()
#             if reconciliation.reconciliation_type == "Credit":
#                 reconciliation.shop.wallet += reconciliation_item.price
#             reconciliation.shop.save()
#         return UpdateReconciliation(reconciliation=reconciliation)


class ReconciliationMutation(graphene.ObjectType):
    create_reconciliation = CreateReconciliation.Field()
    # update_reconciliation = UpdateReconciliation.Field()
