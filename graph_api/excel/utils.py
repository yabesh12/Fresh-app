import pandas as pd
from django.db import transaction
from graphql import GraphQLError

from group.models import PriceGroup, GroupBasedPrice
from product.models import ProductType, Category, Product
import json


def validate_input_file(self, info, **kwargs):
    """
    validate the input file is in correct format otherwise throw error
    """
    file = info.context.FILES.get('file')
    allowed_content_types = [
        'application/vnd.oasis.opendocument.spreadsheet',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
    ]
    print(file.content_type)
    if file is None:
        raise GraphQLError('No File Uploaded.')
    if file.content_type not in allowed_content_types:
        raise GraphQLError('Invalid File Format')
    return file


def import_data_from_excel(file):
    """
    Extracts Data from Excel and Populates in DB Tables
    """
    df = pd.read_excel(file)
    price_group_df = df[
        ['price_group_name', 'price_group_is_active']
    ]

    group_based_prices_df = df[
        ['price_group_name', 'product_sku', 'pro_selling_price', 'pro_discount_selling_price']
    ]

    price_groups = [json.loads(price_group_df.loc[pg].to_json()) for pg in price_group_df.index]
    group_based_prices = [json.loads(group_based_prices_df.loc[gp_pr].to_json()) for gp_pr in
                          group_based_prices_df.index]
    for pg in price_groups:
        name = pg.get('price_group_name')
        is_active = pg.get('price_group_is_active')
        PriceGroup.objects.get_or_create(
            name=name,
            is_active=False if int(is_active) == 0 else True)
    for gp_pr in group_based_prices:
        pr_group = gp_pr.get('price_group_name')
        selling_price = gp_pr.get('pro_selling_price')
        product = gp_pr.get('product_sku')
        discount_selling_price = gp_pr.get('pro_discount_selling_price')
        try:
            price_group_obj = PriceGroup.objects.get(name=pr_group)
        except PriceGroup.DoesNotExist:
            continue
        try:
            product_obj = Product.objects.get(sku=product)
        except Product.DoesNotExist:
            continue
        if product_obj.base_price <= selling_price <= product_obj.mrp_price:
            GroupBasedPrice.objects.update_or_create(
                price_group=price_group_obj,
                product=product_obj,
                defaults={
                    'selling_price': selling_price,
                    'discount_selling_price': discount_selling_price,
                }
            )
        else:
            continue
    message = "Data Might be populated. If something is missing Please Check your Excel Sheet If the data entry is valid " \
              "format."

    return message


def populate_data_from_excel(file):
    """
    Extracts Data from Excel and Populates in Product, ProductType, Category Models
    """
    df = pd.read_excel(file)
    product_types_df = df[['pt_title', 'pt_unit', 'pt_tax', 'pt_is_credit_available', 'pt_is_active']]
    categories_df = df[['cat_name', 'cat_is_active', 'cat_parent', 'cat_product_type']]
    products_df = df[['pro_name', 'sku', 'shelf_life', 'base_price', 'selling_price', 'mrp_price',
                      'pro_unit', 'pro_weight', 'pro_is_active', 'pro_parent', 'pro_product_type', 'pro_category']]
    product_types = [json.loads(product_types_df.loc[pt_df].to_json()) for pt_df in product_types_df.index]
    categories = [json.loads(categories_df.loc[cat_dt].to_json()) for cat_dt in categories_df.index]
    products = [json.loads(products_df.loc[pro_dt].to_json()) for pro_dt in products_df.index]
    for pt in product_types:
        title = pt.get('pt_title')
        if ProductType.objects.filter(title=title).exists():
            continue
        unit = pt.get('pt_unit')
        tax = pt.get('pt_tax')
        credit_status = pt.get('pt_is_credit_available')
        active_status = pt.get('pt_is_active')
        if type(tax) != float:
            tax = None
        if title is not None and unit is not None and tax is not None and credit_status is not None and active_status is not None:
            ProductType.objects.get_or_create(
                title=title,
                unit=unit,
                tax=tax,
                is_credit_available=False if int(credit_status) == 0 else True,
                is_active=False if int(active_status) == 0 else True)
    for cat in categories:
        name = cat.get('cat_name')
        if Category.objects.filter(name=name).exists():
            continue
        active_status = cat.get('cat_is_active')
        parent = cat.get('cat_parent')
        product_type = cat.get('cat_product_type')
        if name is not None and active_status is not None:
            try:
                product_type = ProductType.objects.get(title=product_type)
            except ProductType.DoesNotExist:
                product_type = None
            try:
                parent_category = Category.objects.get(name=parent)
            except Category.DoesNotExist:
                parent_category = None
            Category.objects.get_or_create(
                name=name,
                is_active=False if int(active_status) == 0 else True,
                product_type=product_type,
                parent=parent_category
            )
    for product in products:
        sku = product.get('sku')
        if Product.objects.filter(sku=sku).exists():
            continue
        name = product.get('pro_name')
        shelf_life = product.get('shelf_life')
        base_price = product.get('base_price')
        selling_price = product.get('selling_price')
        mrp_price = product.get('mrp_price')
        unit = product.get('pro_unit')
        weight = product.get('pro_weight')
        active_status = product.get('pro_is_active')
        parent = product.get('pro_parent')
        product_type = product.get('pro_product_type')
        category = product.get('pro_category')
        if type(shelf_life) != int and type(shelf_life) != float:
            shelf_life = None
        if type(base_price) != float and type(base_price) != int:
            base_price = None
        if type(selling_price) != float and type(selling_price) != int:
            selling_price = None
        if type(mrp_price) != float and type(mrp_price) != int:
            mrp_price = None
        if (name is not None and sku is not None and base_price is not None and selling_price is not None
                and mrp_price is not None and shelf_life is not None and unit is not None
                and weight is not None and active_status is not None):
            try:
                parent_product = Product.objects.get(name=parent)
            except Product.DoesNotExist:
                parent_product = None
            try:
                product_type = ProductType.objects.get(title=product_type)
            except ProductType.DoesNotExist:
                product_type = None
            try:
                category = Category.objects.get(name=category)
            except Category.DoesNotExist:
                category = None
            Product.objects.get_or_create(
                name=name,
                sku=sku,
                shelf_life=shelf_life,
                base_price=base_price,
                selling_price=selling_price,
                mrp_price=mrp_price,
                unit=unit,
                weight=weight,
                is_active=False if int(active_status) == 0 else True,
                parent=parent_product,
                product_type=product_type,
                category=category
            )
    return "Data Might be populated. If something is missing Please Check your Excel Sheet If the data entry is valid " \
           "format."
