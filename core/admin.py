from django.contrib import admin
from core.models import Vendor, Products

# Register your models here.
@admin.register(Vendor)
class Vendor(admin.ModelAdmin):
    list_display = ['id', 'name', 'cnpj_vendor', 'city']
    search_fields = ('id', 'name', 'cnpj_vendor', 'city')


@admin.register(Products)
class Products(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'price', 'vendor']
    search_fields = ('id', 'name', 'code', 'price', 'vendor')