import graphene
import graphql_jwt

from graph_api.accounts.mutations import AccountMutation
from graph_api.accounts.schema import GetAllUsers
from graph_api.category.mutations import CategoryMutation
from graph_api.category.schema import CategoryQuery
from graph_api.credit.mutations import CreditMutation
from graph_api.excel.mutations import FileImportMutation
from graph_api.group.mutations import GroupMutation
from graph_api.group.schema import PriceGroupQuery
from graph_api.inventory.mutations import InventoryMutation
from graph_api.inventory.schema import InventoryQuery
from graph_api.order.mutations import OrderMutation
from graph_api.order.schema import OrderQuery
from graph_api.product.mutations import ProductMutation
from graph_api.product.schema import ProductQuery
from graph_api.product_type.mutations import ProductTypeMutation
from graph_api.product_type.schema import ProductTypeQuery
from graph_api.reconciliation.mutation import ReconciliationMutation
from graph_api.reconciliation.schema import ReconciliationQuery
from graph_api.request.mutations import RequestMutation
from graph_api.request.schema import RequestQuery
from graph_api.route.mutations import RouteMutation
from graph_api.route.schema import RouteQuery
from graph_api.sales_executive.mutations import SalesExecutiveMutation
from graph_api.sales_executive.schema import SalesExecutiveQuery
from graph_api.shop.mutations import ShopMutation
from graph_api.shop.schema import ShopQuery
from graph_api.transaction.schema import TransactionQuery


class Query(GetAllUsers, CategoryQuery, ProductQuery, ProductTypeQuery, RouteQuery, PriceGroupQuery,
            ShopQuery, RequestQuery, SalesExecutiveQuery, ReconciliationQuery, InventoryQuery, OrderQuery,
            graphene.ObjectType):
    pass


class Mutation(AccountMutation, CategoryMutation, ProductMutation, ProductTypeMutation, RouteMutation,
               SalesExecutiveMutation, GroupMutation, ShopMutation, FileImportMutation, InventoryMutation,
               CreditMutation, RequestMutation,
               ReconciliationMutation, TransactionQuery, OrderMutation,
               graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(mutation=Mutation, query=Query)
