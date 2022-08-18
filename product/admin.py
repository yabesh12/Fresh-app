from django.contrib import admin

# Register your models here.
from product.models import ProductType, Category, Product

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ProductTypeResource(resources.ModelResource):
    class Meta:
        model = ProductType
        fields = "__all__"


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = "__all__"


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = "__all__"


class ProductTypeResourceAdmin(ImportExportModelAdmin):
    resource_class = ProductTypeResource
    list_display = ("id", "title", "unit", "tax", "is_credit_available", "is_active", "is_deleted",)


class CategoryResourceAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ("id", "product_type", "name", "is_active", "is_deleted",)


class ProductResourceAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = (
        "id", "product_type", "category", "parent", "name", "sku", "shelf_life", "base_price", "selling_price",
        "mrp_price", "is_deleted",)


admin.site.register(ProductType, ProductTypeResourceAdmin)
admin.site.register(Category, CategoryResourceAdmin)
admin.site.register(Product, ProductResourceAdmin)
