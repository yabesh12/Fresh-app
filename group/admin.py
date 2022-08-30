from django.contrib import admin

from group.models import PriceGroup, GroupBasedPrice


class GroupBasedPriceInline(admin.StackedInline):
    model = GroupBasedPrice
    extra = 0


class GroupBasedPriceInlineAdmin(admin.ModelAdmin):
    inlines = [
        GroupBasedPriceInline,
    ]


admin.site.register(PriceGroup, GroupBasedPriceInlineAdmin)
