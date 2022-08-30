import graphene
from django.shortcuts import get_object_or_404
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from graph_api.accounts.decorators import manager_only
from graph_api.shop.utils import get_validate_shop_arguments
from group.models import PriceGroup
from shop.models import Shop


class CreateShop(graphene.Mutation):
    """
    Only manager can Create shop if shop is not exists
    """

    class Arguments:
        price_group_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        place = graphene.String(required=True)
        address = graphene.String(required=True)
        gst_number = graphene.String()
        phone_number = graphene.String()
        wallet = graphene.Decimal()
        total_credit_limit = graphene.Decimal()
        total_credit = graphene.Decimal()
        is_chain = graphene.Boolean()
        is_active = graphene.Boolean(required=True)

    status = graphene.String()
    message = graphene.String()

    @login_required
    @manager_only
    def mutate(self, info, price_group_id, name, place, address, is_active, **kwargs):
        price_group_obj = get_object_or_404(PriceGroup, id=price_group_id)

        gst_number, phone_number, wallet, total_credit_limit, total_credit, is_chain, is_deleted = get_validate_shop_arguments(
            **kwargs)

        try:
            shop_obj, _ = Shop.objects.get_or_create(name=name, price_group=price_group_obj,
                                                     place=place, address=address, gst_number=gst_number,
                                                     phone_number=phone_number, wallet=wallet,
                                                     total_credit_limit=total_credit_limit, total_credit=total_credit,
                                                     is_chain=is_chain, is_deleted=is_deleted,
                                                     is_active=is_active)
        except Exception as e:
            return e

        return CreateShop(status="ok", message="Added new Shop successfully.")


class UpdateShop(graphene.Mutation):
    """
    Update Shop details only by Manager
    """

    class Arguments:
        shop_id = graphene.ID(required=True)
        price_group_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        place = graphene.String(required=True)
        address = graphene.String(required=True)
        gst_number = graphene.String()
        phone_number = graphene.String()
        wallet = graphene.Decimal()
        total_credit_limit = graphene.Decimal()
        total_credit = graphene.Decimal()
        is_chain = graphene.Boolean()
        is_active = graphene.Boolean(required=True)

    status = graphene.String()
    message = graphene.String()

    @login_required
    @manager_only
    def mutate(self, info, shop_id, price_group_id, name, place, address, is_active, **kwargs):
        gst_number, phone_number, wallet, total_credit_limit, total_credit, is_chain, is_deleted = get_validate_shop_arguments(
            **kwargs)
        try:
            shop_obj = Shop.objects.filter(id=shop_id, price_group_id=price_group_id).exclude(is_deleted=True).first()
            if shop_obj is not None:
                shop_obj.name = name
                shop_obj.place = place
                shop_obj.address = address
                shop_obj.gst_number = gst_number
                shop_obj.wallet = wallet
                shop_obj.total_credit_limit = total_credit_limit
                shop_obj.total_credit = total_credit
                shop_obj.is_chain = is_chain
                shop_obj.is_active = is_active
                shop_obj.is_deleted = is_deleted
                shop_obj.save(force_update=True)
            else:
                raise GraphQLError("shop is not exists.")
        except Exception as e:
            return e

        return UpdateShop(status="Ok", message=f"Shop {shop_obj.name} is successfully updated.")


class DeleteShop(graphene.Mutation):
    """
    Delete particular Shop details only by Manager
    """

    class Arguments:
        shop_id = graphene.ID(required=True)
        price_group_id = graphene.ID(required=True)

    status = graphene.String()
    message = graphene.String()

    def mutate(self, info, shop_id, price_group_id, **kwargs):

        try:
            shop_obj = Shop.objects.get(id=shop_id, price_group_id=price_group_id)
            shop_obj.is_deleted = True
            shop_obj.save(update_fields=['is_deleted'])

        except Shop.DoesNotExist:
            raise GraphQLError(f'Invalid Shop {shop_obj.name}.')

        return DeleteShop(status="Ok", message=f'Successfully deleted the shop {shop_obj.name}.')


class ShopMutation(graphene.ObjectType):
    create_shop = CreateShop.Field()
    update_shop = UpdateShop.Field()
    delete_shop = DeleteShop.Field()
