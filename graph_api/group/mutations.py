from functools import reduce

import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from graph_api.accounts.decorators import manager_only, admin_only
from graph_api.group.input import GroupBasedPricesInput
from group.models import PriceGroup, GroupBasedPrice
from product.models import Product


class CreateUpdatePriceGroup(graphene.Mutation):
    """
    Manager and Admin can only
    -> Create Price Group, Group based prices
    -> Update Price Group, Group based prices

    """

    class Arguments:
        name = graphene.String(required=True)
        group_based_prices = graphene.List(GroupBasedPricesInput)
        is_active = graphene.Boolean()

    status = graphene.String()
    message = graphene.String()
    invalid_sku = graphene.String()
    invalid_selling_price = graphene.String()

    @login_required
    @manager_only
    def mutate(self, info, name, group_based_prices, **kwargs):
        try:
            price_group_obj, _ = PriceGroup.objects.get_or_create(name=name,
                                                                  defaults={'is_active': kwargs.get('is_active', True)})
            invalid_sku = []
            invalid_selling_price = {}

            # Create or Update the group based prices
            def create_or_update_group_based_prices(group_based_prices):
                discount_selling_price = group_based_prices.get('discount_selling_price', 0)
                product = Product.objects.filter(sku=group_based_prices.product_sku)
                if product.exists():
                    product_obj = product.first()

                    # Selling price should not exceed the MRP price and lower than the Base price
                    if product_obj.base_price <= group_based_prices.selling_price <= product_obj.mrp_price:
                        print("pro")
                        GroupBasedPrice.objects.update_or_create(
                            price_group=price_group_obj,
                            product=product_obj,
                            defaults={'selling_price': group_based_prices.selling_price,
                                      'discount_selling_price': discount_selling_price},
                        )
                    else:
                        invalid_selling_price[group_based_prices.product_sku] = group_based_prices.selling_price

                else:
                    invalid_sku.append(group_based_prices.product_sku)

            list(map(create_or_update_group_based_prices, group_based_prices))

            msg = "Added new Price Group successfully."
            inv_sku = "Invalid Sku " + ",".join(str(x) for x in invalid_sku)
            inv_sell_price = "product's selling price should not exceed MRP price and should not lower than base " \
                             "price for product " + ",".join(str(x) for x, y in invalid_selling_price.items())

            if len(invalid_sku) > 0 and len(invalid_selling_price) > 0:
                return CreateUpdatePriceGroup(status="ok", message=msg,
                                              invalid_sku=inv_sku,
                                              invalid_selling_price=inv_sell_price)
            if len(invalid_sku) > 0:
                return CreateUpdatePriceGroup(status="ok", message=msg,
                                              invalid_sku=inv_sku)
            if len(invalid_selling_price) > 0:
                return CreateUpdatePriceGroup(status="ok", message=msg, invalid_selling_price=inv_sell_price)

        except Exception as e:
            return e

        return CreateUpdatePriceGroup(status="ok", message=msg)


class DeletePriceGroup(graphene.Mutation):
    """
    Admin can
    -> Remove the Price Group

    """

    class Arguments:
        price_group_id = graphene.ID(required=True)

    status = graphene.String()
    message = graphene.String()

    # @login_required
    # @admin_only
    def mutate(self, info, price_group_id, **kwargs):

        try:
            price_group_obj = PriceGroup.objects.get(id=price_group_id)
            price_group_obj.is_deleted = True
            price_group_obj.save(update_fields=['is_deleted'])

        except PriceGroup.DoesNotExist:
            raise GraphQLError("Invalid Price Group!")

        return DeletePriceGroup(status="Ok", message="Successfully deleted the Price Group.")


class GroupMutation(graphene.ObjectType):
    create_update_price_group = CreateUpdatePriceGroup.Field()
    delete_price_group = DeletePriceGroup.Field()
