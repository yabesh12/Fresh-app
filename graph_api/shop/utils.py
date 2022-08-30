from decimal import Decimal

from graph_api.core.utils import validate_mobile_number


def get_validate_shop_arguments(**kwargs):
    gst_number = kwargs.get('gst_number')
    phone_number = kwargs.get('phone_number')
    wallet = kwargs.get('wallet', Decimal(0.0))
    total_credit_limit = kwargs.get('total_credit_limit', Decimal(0.0))
    total_credit = kwargs.get('total_credit', Decimal(0.0))
    is_chain = kwargs.get('is_chain', False)
    is_deleted = kwargs.get('is_deleted', False)
    validate_mobile_number(phone_number)
    return gst_number, phone_number, wallet, total_credit_limit, total_credit, is_chain, is_deleted