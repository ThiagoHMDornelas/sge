from django.contrib import admin

from core.admin import BaseAdmin
from . import models


class BrandAdmin(BaseAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name',)


admin.site.register(models.Brand, BrandAdmin)
