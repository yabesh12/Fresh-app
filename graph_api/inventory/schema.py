import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graph_api.inventory.type import InventoryType
from sales_executive.models import Inventory


class InventoryQuery(graphene.ObjectType):
    inventory_by_id = graphene.Field(InventoryType, inventory_id=graphene.ID())
    all_inventories = graphene.List(InventoryType)

    @login_required
    def resolve_inventory_by_id(self, info, inventory_id):
        user = info.context.user
        if user.is_manager:
            try:
                inventory = Inventory.objects.get(id=inventory_id)
            except Inventory.DoesNotExist:
                raise GraphQLError(f'Invalid Inventory!')
            return inventory
        try:
            inventory = Inventory.objects.get(id=inventory_id, sales_executive__user=user)
        except Inventory.DoesNotExist:
            raise GraphQLError(f'Invalid Inventory!')
        return inventory

    @login_required
    def resolve_all_inventories(self, info):
        user = info.context.user
        if user.is_manager:
            return Inventory.objects.all().order_by('-created_at')
        return Inventory.objects.filter(sales_executive__user=user).order_by('-created_at')