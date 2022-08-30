import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from graph_api.accounts.decorators import manager_only
from .utils import populate_data_from_excel, validate_input_file, import_data_from_excel


class ProductTypeCategoryProductDataPopulate(graphene.Mutation):
    """
    ProductType Category Product Data Populate from excel to db
    """
    message = graphene.String()

    @login_required
    @manager_only
    def mutate(self, info):
        file = info.context.FILES.get('file')
        allowed_content_types = [
            'application/vnd.oasis.opendocument.spreadsheet',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-excel',
        ]
        if file is None:
            raise GraphQLError('No File Uploaded.')
        if file.content_type not in allowed_content_types:
            raise GraphQLError('Invalid File Format')
        message = populate_data_from_excel(file)
        return ProductTypeCategoryProductDataPopulate(message=message)


class PriceGroupImport(graphene.Mutation):
    """
    Price group and Group based prices import only by manager
    """
    status = graphene.String()
    message = graphene.String()

    @login_required
    @manager_only
    def mutate(self, info, **kwargs):
        file = validate_input_file(self, info)
        message = import_data_from_excel(file)
        return PriceGroupImport(status="Ok", message=message)


class FileImportMutation(graphene.ObjectType):
    populate_category_product_product_type_data = ProductTypeCategoryProductDataPopulate.Field()
    price_group_import = PriceGroupImport.Field()
