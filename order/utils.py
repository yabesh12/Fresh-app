from django.db.models import Sum, OuterRef, Subquery, F, Value, IntegerField
from django.db.models.functions import Round, Coalesce

from credit.models import CreditLimit, Credit
from product.models import Category


def credit_availability_check_based_on_category_limit(shop_obj, order_obj, safe_mode=False):
    """
    !This function is used to check the credit availability for the shop
    :param shop_obj:
    :param order_obj:
    :param safe_mode:
    :return:
    """
    order_obj.refresh_from_db()
    credit_limit_obj = CreditLimit.objects.filter(shop=shop_obj, category=OuterRef('pk')).annotate(
        limit=Coalesce(Round(F('shop__total_credit_limit') * F('percentage') / 100), Value(0),
                       output_field=IntegerField()))
    credit_obj = Credit.objects.filter(shop=shop_obj, category_id=OuterRef('pk'))[:1]
    order_items = order_obj.order_items.all()
    categories = order_items.values_list('product__category_id', flat=True).distinct()
    print(categories)
    order_item_subquery = order_items.filter(product__category_id=OuterRef('pk')).annotate(
        category=F('product__category_id')).values('category').annotate(
        category_based_total=Sum('total')).values('category_based_total')[:1]
    category_obj = Category.objects.filter(id__in=categories).annotate(
        category_credit_limit=Subquery(credit_limit_obj.values('limit')),
        category_credit_amount=Subquery(credit_obj.values('amount')),
        category_credit_available=Round(
            F('category_credit_limit') - F('category_credit_amount')
        ),
        order_amount=Subquery(order_item_subquery),
    )
    # Check if the credit is available for the shop
    category_and_available_credits = []
    for category in category_obj:
        """
        condition need to be checked:
            - credit limit should be greater than or equal to the order amount + current credit amount
        """
        if (category.category_credit_available or 0) < (
                category.order_amount + category.category_credit_amount) and category.product_type.is_credit_available:
            if safe_mode:
                category_and_available_credits.append(
                    {
                        "category_id": category.pk,
                        "category_name": category.name,
                        "credit_limit": category.category_credit_limit or 0,
                        "credit_amount": category.category_credit_amount,
                        "credit_available": category.category_credit_available or 0,
                        "order_amount": category.order_amount,
                        "is_credit_available": category.product_type.is_credit_available,
                        "status": "Credit not available or Reached the limit"
                    })
            else:
                raise Exception(
                    f'Credit is not available for the shop {shop_obj.name} for the category {category.name}')
        else:
            category_and_available_credits.append(
                {
                    "category_id": category.pk,
                    "category_name": category.name,
                    "credit_limit": category.category_credit_limit,
                    "credit_amount": category.category_credit_amount,
                    "credit_available": category.category_credit_available,
                    "order_amount": category.order_amount,
                    "is_credit_available": category.product_type.is_credit_available,
                    "status": "Credit available"
                })
    return category_and_available_credits


def credit_amount_split_data(order_obj, shop_obj, payment_data):
    """
    !This function is used to split the credit amount based on the category
    :param order_obj:
    :param shop_obj:
    :param payment_data:
    :return:
    """
    credit_available_data = credit_availability_check_based_on_category_limit(shop_obj, order_obj, safe_mode=True)

    payment_data2 = []
    credited_amount_total = 0
    for credit_data in credit_available_data:
        category_id = credit_data.get('category_id')
        filtered_data = list(filter(lambda x: x.get('category_id') == category_id, payment_data))
        if type(filtered_data) is list:
            amount = filtered_data[0].get('amount', 0)
            available_credit_amount = credit_data.get('credit_available', 0)
            order_amount = credit_data.get('order_amount', 0)
            if float(available_credit_amount) < float(float(order_amount) - float(amount)):
                raise Exception(
                    f'Credit is not available for the shop {shop_obj.name} for '
                    f'the category {credit_data.get("category_name")} or reached the limit')
            elif float(order_amount) < float(amount):
                credit_amount = credit_data.get('credit_amount', 0)
                if float(credit_amount) < float(float(amount) - float(order_amount)):
                    raise Exception(
                        "You Cant Pay More Than Your Credit Amount")
                else:
                    payment_data2.append(
                        {
                            "category_id": category_id,
                            "amount": float(order_amount) - float(amount),
                            "shop_id": shop_obj.id
                        }
                    )
                    credited_amount_total += (float(order_amount) - float(amount))
                continue
            elif float(available_credit_amount) >= float(float(amount) - float(order_amount)):
                payment_data2.append(
                    {
                        "category_id": category_id,
                        "amount": float(order_amount) - float(amount),
                        "shop_id": shop_obj.id
                    }
                )
                credited_amount_total += (float(order_amount) - float(amount))
                continue
    return payment_data2, credited_amount_total


def get_credit_amount_for_shop(shop_obj):
    """
    !This function is used to get the credit amount for the shop
    :param shop_obj:
    :return:
    """
    credit_obj = Credit.objects.filter(shop=shop_obj)
    credit_amount = credit_obj.aggregate(credit_amount=Sum('amount')).get('credit_amount', 0)
    return credit_amount
