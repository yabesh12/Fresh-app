import graphene
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from credit.models import Credit
from graph_api.order.enum import PaymentTypeEnum
from graph_api.order.inputs import OrderInput, PaymentPartialInputOrPayBackCreditInput, OrderItemInput
from graph_api.order.type import OrderNode, CreditAvailabilityResponseType
from order.models import Order, OrderItem
from order.utils import credit_availability_check_based_on_category_limit, credit_amount_split_data, \
    get_credit_amount_for_shop
from payment.models import Payment
from product.models import Product
from shop.models import Shop


class CreateOrder(graphene.Mutation):
    """
    Mutation to create a new Order
    -> Requires Login
    -> Requires Sales Executive
    -> check credit limit
    -> Apply reconciliation discount
    -> Apply outstanding credit balance
    -> Calculate total amount
    -> Calculate total tax
    """
    order = graphene.Field(lambda: OrderNode)
    status = graphene.String()
    message = graphene.String()
    credit_availability = graphene.List(lambda: CreditAvailabilityResponseType)

    class Arguments:
        data = graphene.Argument(lambda: OrderInput)

    @login_required
    # @manager_only
    def mutate(self, info, data):
        today = timezone.now().date()
        with transaction.atomic():
            shop_id = data.get('shop_id', '')
            order_items = data.get('order_items', [])
            if shop_id != '':
                shop_id = from_global_id(shop_id)[1]
                try:
                    shop_obj = Shop.objects.get(id=shop_id)
                except Shop.DoesNotExist:
                    raise Exception('Shop does not exist')
                product_objs = Product.custom_shop_manager.get_selling_price_by_group(shop_obj.price_group)
                sales_executive_obj = info.context.user.salesexecutive
                outstanding_credit_balance = get_credit_amount_for_shop(shop_obj)
                order = Order.objects.create(
                    billed_to_id=shop_id,
                    bill_date=today,
                    billed_by=sales_executive_obj,
                    out_standing_credit=outstanding_credit_balance,
                )
                order_items_list = []
                for item in order_items:
                    product_id = item.get('product_id', '')
                    product_id = from_global_id(product_id)[1]
                    quantity = item.get('quantity', 0)
                    try:
                        product_obj = product_objs.get(id=product_id)
                    except Product.DoesNotExist:
                        print("Product Does Not Exist")
                        continue
                    price = product_obj.sell_price
                    order_items_list.append(
                        OrderItem(
                            order=order,
                            product=product_obj,
                            quantity=quantity,
                            price=price,
                            total=price * quantity
                        ))
                OrderItem.objects.bulk_create(order_items_list)

            credit_availability_based_on_category = credit_availability_check_based_on_category_limit(
                shop_obj=shop_obj,
                order_obj=order,
                safe_mode=True
            )
        return CreateOrder(status='success', message='Order Created Successfully!',
                           credit_availability=credit_availability_based_on_category, order=order)


# class UpdateOrder(graphene.Mutation):
#     """
#     Mutation to update an existing Order
#     -> Requires Login
#     -> Requires Sales Executive
#     -> check credit limit
#     -> Apply reconciliation discount
#     -> Apply outstanding credit balance
#     -> Calculate total amount
#     -> Calculate total tax
#     """
#     order = graphene.Field(lambda: OrderNode)
#     status = graphene.String()
#     message = graphene.String()
#     credit_availability = graphene.List(lambda: CreditAvailabilityResponseType)
#
#     class Arguments:
#         data = graphene.Argument(lambda: OrderInput)
#         order_id = graphene.ID(required=True)
#
#     @login_required
#     # @manager_only
#     def mutate(self, info, data):
#         today = timezone.now().date()
#         with transaction.atomic():
#             shop_id = data.get('shop_id', '')
#             route_id = data.get('route_id', '')
#             order_items = data.get('order_items', [])
#             shop_obj = Shop.objects.first()
#             product_objs = Product.custom_shop_manager.get_selling_price_by_group(shop_obj.price_group)
#
#             if shop_id != '' and route_id != '':
#                 shop_id = from_global_id(shop_id)[1]
#                 sales_executive_obj = info.context.user.salesexecutive
#                 order = Order.objects.get(id=from_global_id(data.get('order_id'))[1])
#                 order.billed_to_id = shop_id
#                 # order.route_id = route_id
#                 order.bill_date = today
#                 order.billed_by = sales_executive_obj
#                 order.save()
#                 order_items_list = []
#                 for item in order_items:
#                     product_id = item.get('product_id', '')
#                     product_id = from_global_id(product_id)[1]
#                     quantity = item.get('quantity', 0)
#                     try:
#                         product_obj = product_objs.get(id=product_id)
#                     except Product.DoesNotExist:
#                         print("Product Does Not Exist")
#                         continue
#                     order_item_obj, created = OrderItem.objects.get_or_create(
#                         order=order,
#                         product=product_obj
#                     )
#                     price = product_obj.sell_price
#                     order_item_obj.quantity = quantity
#                     order_item_obj.price = price
#
#                     order_items_list.append(
#                         order_item_obj
#                     )
#                 OrderItem.objects.bulk_update(order_items_list, ['quantity', 'price'])
#                 credit_availability_based_on_category = credit_availability_check_based_on_category_limit(
#                     shop_obj=shop_obj,
#                     order_obj=order,
#                     safe_mode=True
#                 )
#             return UpdateOrder(order=order, status='success', message='Order Updated Successfully!',
#                                credit_availability_based_on_category=credit_availability_based_on_category)


class UpdateOrderItem(graphene.Mutation):
    order = graphene.Field(lambda: OrderNode)
    status = graphene.String()
    message = graphene.String()
    credit_availability = graphene.List(lambda: CreditAvailabilityResponseType)

    class Arguments:
        order_id = graphene.ID(required=True)
        shop_id = graphene.ID(required=True)
        order_item = OrderItemInput(required=True)

    @login_required
    # @manager_only
    def mutate(self, info, order_id, shop_id, order_item):
        with transaction.atomic():
            order_obj = Order.objects.get(id=from_global_id(order_id)[1])
            shop_obj = Shop.objects.get(id=from_global_id(shop_id)[1])
            product_objs = Product.custom_shop_manager.get_selling_price_by_group(shop_obj.price_group)
            product_id = from_global_id(order_item.get('product_id', ''))[1]
            quantity = order_item.get('quantity', 0)
            try:
                product_obj = product_objs.get(id=product_id)
            except Product.DoesNotExist:
                print("Product Does Not Exist")
                return UpdateOrderItem(status='error', message='Product Does Not Exist')
            price = product_obj.sell_price
            order_item_obj, created = OrderItem.objects.get_or_create(
                order=order_obj,
                product=product_obj
            )
            order_item_obj.quantity = quantity
            order_item_obj.price = price
            order_item_obj.save()
            credit_availability_based_on_category = credit_availability_check_based_on_category_limit(
                shop_obj=shop_obj,
                order_obj=order_obj,
                safe_mode=True
            )
        return UpdateOrderItem(status='success', message='Order Item Updated Successfully!',
                               credit_availability=credit_availability_based_on_category,
                               order=order_obj)


class DropOrderItem(graphene.Mutation):
    order = graphene.Field(lambda: OrderNode)
    status = graphene.String()
    message = graphene.String()
    credit_availability = graphene.String()

    class Arguments:
        order_id = graphene.ID(required=True)
        order_item_ids = graphene.List(graphene.ID, required=True)

    @login_required
    def mutate(self, info, order_id, order_item_ids, **kwargs):
        with transaction.atomic():
            try:
                order_obj = Order.objects.get(id=from_global_id(order_id)[1])
                order_item_objs = OrderItem.objects.filter(id__in=order_item_ids)
                order_item_objs.delete()
            except Order.DoesNotExist:
                return DropOrderItem(status='error', message='Order Does Not Exist!')
            if not order_obj.order_items.exists():
                return DropOrderItem(status='error', message='Order Has No Items!')
            credit_availability_based_on_category = credit_availability_check_based_on_category_limit(
                shop_obj=order_obj.billed_to,
                order_obj=order_obj,
                safe_mode=True
            )
        return DropOrderItem(order=order_obj, status='success', message='Order Item Deleted Successfully!',
                             credit_availability_based_on_category=credit_availability_based_on_category)


class CompleteOrder(graphene.Mutation):
    """
    Mutation to complete an existing Order
    -> Requires Login
    -> Requires Sales Executive
    -> check credit limit
    -> Apply reconciliation discount
    -> Apply outstanding credit balance
    -> Calculate total amount
    -> Calculate total tax
    """
    order = graphene.Field(lambda: OrderNode)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        order_id = graphene.ID(required=True)
        shop_id = graphene.ID(required=True)
        payment_type = PaymentTypeEnum(required=True)
        amount = graphene.Float(required=True)
        payment_data = graphene.List(PaymentPartialInputOrPayBackCreditInput, required=True)
        remarks = graphene.String()

    @login_required
    # @manager_only
    def mutate(self, info, order_id, shop_id, payment_type, **kwargs):
        user_obj = info.context.user
        sales_executive_obj = user_obj.salesexecutive
        with transaction.atomic():
            order_id = from_global_id(order_id)[1]
            shop_id = from_global_id(shop_id)[1]
            try:
                order_obj = Order.objects.get(id=order_id, billed_by=sales_executive_obj)
            except Order.DoesNotExist:
                return CompleteOrder(status='error', message='Order Does Not Exist or Invalid Request!')
            try:
                shop_obj = Shop.objects.get(id=shop_id)
            except Shop.DoesNotExist:
                return CompleteOrder(status='error', message='Shop Does Not Exist or Invalid Request!')
            if order_obj.status == 'Pending':
                order_obj.status = 'Completed'
                order_obj.total = order_obj.get_total_amount_or_total_payable
                order_obj.save()
                if payment_type == 'Partial' or payment_type == 'Credit':
                    credit_data, credited_value = credit_amount_split_data(
                        shop_obj=shop_obj,
                        order_obj=order_obj,
                        payment_data=kwargs.get('payment_data', [])
                    )
                    credit_update_list = []
                    for i in credit_data:
                        credit_obj, created = Credit.objects.get_or_create(
                            shop=shop_obj,
                            category_id=i.get('category_id', ''))
                        credit_obj.amount = F('amount') + i.get('amount', 0)
                        credit_update_list.append(credit_obj)
                    Credit.objects.bulk_update(credit_update_list, ['amount'])
                    Payment.objects.create(
                        order=order_obj,
                        shop=shop_obj,
                        amount=credited_value,
                        sales_executive=sales_executive_obj,
                        payment_type="CREDIT",
                        remarks=kwargs.get('remarks', '')
                    )
                    if payment_type == 'Partial':
                        Payment.objects.create(
                            order=order_obj,
                            shop=shop_obj,
                            sales_executive=sales_executive_obj,
                            amount=kwargs.get('amount', 0),
                            remarks=kwargs.get('remarks', ''),
                        )
                elif payment_type == 'Full':
                    amount_paid = kwargs.get('amount', 0)
                    if float(amount_paid) == 0 or amount_paid is None:
                        return CompleteOrder(status='error', message='Amount Paid Cannot Be Zero!')
                    if float(amount_paid) == float(order_obj.get_total_amount_or_total_payable):
                        # updated the available credit amount to zero
                        Credit.objects.filter(shop=shop_obj).update(
                            amount=0
                        )
                        Payment.objects.create(
                            order=order_obj,
                            shop=shop_obj,
                            amount=amount_paid,
                            sales_executive=sales_executive_obj,
                            remarks=kwargs.get('remarks', ''),
                        )
                    else:
                        raise Exception('Amount Paid Cannot Be Less Than Or Greater Than Total Amount!')
                return CompleteOrder(order=order_obj, status='success', message='Order Completed Successfully!')
            else:
                raise Exception('Order Already Completed!')


class ApplyWalletAmount(graphene.Mutation):
    class Arguments:
        order_id = graphene.ID(required=True)
        shop_id = graphene.ID(required=True)
        amount = graphene.Float(required=True)

    order = graphene.Field(lambda: OrderNode)
    status = graphene.String()
    message = graphene.String()

    @login_required
    def mutate(self, info, order_id, shop_id, amount, **kwargs):
        user_obj = info.context.user
        sales_executive_obj = user_obj.salesexecutive
        with transaction.atomic():
            order_id = from_global_id(order_id)[1]
            shop_id = from_global_id(shop_id)[1]
            try:
                order_obj = Order.objects.get(id=order_id, billed_by=sales_executive_obj)
            except Order.DoesNotExist:
                return ApplyWalletAmount(status='error', message='Order Does Not Exist or Invalid Request!')
            try:
                shop_obj = Shop.objects.get(id=shop_id)
            except Shop.DoesNotExist:
                return ApplyWalletAmount(status='error', message='Shop Does Not Exist or Invalid Request!')
            if order_obj.status == 'Pending':
                wallet_money = shop_obj.wallet
                if wallet_money < amount:
                    raise Exception('Insufficient Wallet Balance!')
                if wallet_money >= amount:
                    shop_obj.wallet = F('wallet') - amount
                    shop_obj.save()
                    order_obj.discount = amount
                    order_obj.save(update_fields=['discount'])
                    return ApplyWalletAmount(order=order_obj, status='success',
                                             message='Wallet Amount Applied Successfully!')
            else:
                raise Exception('You Cannot Apply Wallet Amount To Completed Order!')


class OrderMutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    drop_order_item = DropOrderItem.Field()
    update_order_item = UpdateOrderItem.Field()
    complete_order = CompleteOrder.Field()
    apply_wallet_amount = ApplyWalletAmount.Field()
