from django.contrib import admin

# Register your models here.
from route.models import Route


class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'is_deleted',)


admin.site.register(Route, RouteAdmin)
