from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'serie_number',)
    search_fields = ('name',)


admin.site.register(models.Product, ProductAdmin)
