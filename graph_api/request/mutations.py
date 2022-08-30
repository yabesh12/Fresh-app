import datetime

import graphene
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from graph_api.request.input import RequestedProductsInput
from product.models import Product
from request.models import Request, RequestItem
from sales_executive.models import SalesExecutive
from shop.models import Shop

User = get_user_model()


class CreateRequest(graphene.Mutation):
    class Arguments:
        shop_id = graphene.ID(required=True)
        due_date = graphene.DateTime(required=True)
        is_active = graphene.Boolean(required=True)
        requested_products = graphene.List(RequestedProductsInput)

    status = graphene.String()
    message = graphene.String()
    invalid_product = graphene.String()

    @login_required
    def mutate(self, info, shop_id, due_date, is_active, requested_products, **kwargs):
        sales_executive = info.context.user
        try:
            shop_obj = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            raise GraphQLError("Shop does not exists!")
        try:
            sales_executive_obj = SalesExecutive.objects.get(user=sales_executive)
        except SalesExecutive.DoesNotExist:
            raise GraphQLError("SalesExecutive does not exists!")
        try:
            request_obj = Request.objects.create(sales_executive=sales_executive_obj, shop=shop_obj,
                                                 requested_date=datetime.datetime.now(),
                                                 due_date=due_date,
                                                 is_active=is_active)
            invalid_pro = []
            requested_products_list = []
            for value in requested_products:
                product = Product.objects.filter(id=value.product_id)
                if product.exists():
                    product_obj = product.first()
                    requested_products_list.append(
                        RequestItem(request=request_obj, product=product_obj, quantity=value.quantity))
                else:
                    invalid_pro.append(value.product_id)

            RequestItem.objects.bulk_create(requested_products_list)
            msg = "Created Request Successfully."


        except Exception as e:
            return e

        if len(invalid_pro) >= 0:
            inv_pro = " ".join([f"Invalid Product {x}" for x in invalid_pro])

        return CreateRequest(status="Ok", message=msg, invalid_product=inv_pro)


class RequestMutation(graphene.ObjectType):
    create_request = CreateRequest.Field()
