import graphene


class InventoryProductStockUpdateInput(graphene.InputObjectType):
    product_sku = graphene.String(required=True)
    stock = graphene.Int(required=True)
    incoming_type = graphene.String(required=True)
