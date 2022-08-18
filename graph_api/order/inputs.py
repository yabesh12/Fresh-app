import graphene


class OrderItemInput(graphene.InputObjectType):
    """
    Input type for OrderItem
    """
    product_id = graphene.ID(required=True)
    quantity = graphene.Int(required=True)


class OrderInput(graphene.InputObjectType):
    """
    Input type for Order
    """
    shop_id = graphene.ID(required=True)
    order_items = graphene.List(OrderItemInput, required=True)


class PaymentPartialInputOrPayBackCreditInput(graphene.InputObjectType):
    """
    Input type for PartialPayment
    """
    category_id = graphene.Int(required=True, description='Category ID It should be an Integer')
    amount = graphene.Float(required=True, description='Amount to be paid for this category')

