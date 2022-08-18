import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from graph_api.accounts.decorators import manager_only, admin_only
from graph_api.group.input import GroupBasedPricesInput
from group.models import PriceGroup, GroupBasedPrice
from product.models import Product


class CreateUpdatePriceGroup(graphene.Mutation):
    """
    Manager can only
    -> Create Price Group
    -> Update Price Group

    """

    class Arguments:
        name = graphene.String(required=True)
        is_active = graphene.Boolean(required=True)
        group_based_prices = graphene.List(GroupBasedPricesInput)

    status = graphene.String()
    message = graphene.String()
    invalid_sku = graphene.String()
    invalid_selling_price = graphene.String()

    @login_required
    @manager_only
    def mutate(self, info, name, is_active, group_based_prices, **kwargs):
        try:
            price_group_obj, _ = PriceGroup.objects.get_or_create(name=name,
                                                                  defaults={'is_active': is_active})
            invalid_sku = []
            invalid_selling_price = {}

            # Create or Update the group based prices
            for value in group_based_prices:
                discount_selling_price = kwargs.get('value.discount_selling_price')
                product = Product.objects.filter(sku=value.product_sku)
                if product.exists():
                    product_obj = product.first()

                    # Selling price should not exceed the MRP price and lower than the Base price
                    if product_obj.base_price <= value.selling_price <= product_obj.mrp_price:
                        group_based_price_objs, created = GroupBasedPrice.objects.update_or_create(
                            price_group=price_group_obj,
                            product=product_obj,
                            defaults={'selling_price': value.selling_price,
                                      'discount_selling_price': discount_selling_price},
                        )
                    else:
                        invalid_selling_price[value.product_sku] = value.selling_price

                else:
                    invalid_sku.append(value.product_sku)

            msg = "Added new Price Group successfully."
            inv_sku = " ".join([f"Invalid Sku {x}" for x in invalid_sku])
            inv_sell_price = " ".join([
                f"product's selling price Rs.{y} should not exceed MRP price and should not lower than base price for product {x}"
                for x, y in
                invalid_selling_price.items()])

            if len(invalid_sku) >= 0 and len(invalid_selling_price) >= 0:
                return CreateUpdatePriceGroup(status="ok", message=msg,
                                              invalid_sku=inv_sku,
                                              invalid_selling_price=inv_sell_price)
            if len(invalid_sku) >= 0:
                return CreateUpdatePriceGroup(status="ok", message=msg,
                                              invalid_sku=inv_sku)
            if len(invalid_selling_price) >= 0:
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

    message = graphene.String()

    @login_required
    @admin_only
    def mutate(self, info, price_group_id, **kwargs):

        try:
            price_group_obj = PriceGroup.objects.get(id=price_group_id)
            price_group_obj.delete()

        except PriceGroup.DoesNotExist:
            raise GraphQLError("Invalid Price Group!")

        return DeletePriceGroup(message="Successfully deleted the Price Group.")


class GroupMutation(graphene.ObjectType):
    create_update_price_group = CreateUpdatePriceGroup.Field()
    delete_price_group = DeletePriceGroup.Field()
