import graphene


class PaymentTypeEnum(graphene.Enum):
    """
    Enum for Payment Type
    """
    FULL = 'Full'
    CREDIT = 'Credit'
    PARTIAL = 'Partial'
