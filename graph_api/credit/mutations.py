import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from credit.models import CreditLimit
from graph_api.accounts.decorators import manager_only
from product.models import Category
from shop.models import Shop


class CreateUpdateCreditLimit(graphene.Mutation):
    """
    Only Manager can Create or Update the Credit Limit for Shop
    """
    class Arguments:
        category_id = graphene.ID(required=True)
        shop_id = graphene.ID(required=True)
        percentage = graphene.Int(required=True)

    status = graphene.String()
    message = graphene.String()

    @login_required
    @manager_only
    def mutate(self, info, category_id, shop_id, percentage, **kwargs):
        try:
            category_obj = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise GraphQLError("Category does not exists.")

        try:
            shop_obj = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            raise GraphQLError("Shop does not exists.")
        try:
            credit_limit, created = CreditLimit.objects.update_or_create(category=category_obj, shop=shop_obj,
                                                                     defaults={'percentage': percentage})
            if not created:
                msg = f"Credit Limit successfully updated for category {credit_limit.category}."
            else:
                msg = f"Credit Limit successfully created for category {credit_limit.category}."
        except Exception as e:
            return e

        return CreateUpdateCreditLimit(status="Ok", message=msg)


class CreditMutation(graphene.ObjectType):
    create_update_credit_limit = CreateUpdateCreditLimit.Field()
