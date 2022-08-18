import graphene


class RequestedProductsInput(graphene.InputObjectType):
    product_id = graphene.String(required=True)
    quantity = graphene.Int(required=True)
