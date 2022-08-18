import graphene


class GroupBasedPricesInput(graphene.InputObjectType):
    product_sku = graphene.String(required=True)
    selling_price = graphene.Decimal(required=True)
    discount_selling_price = graphene.Decimal()
