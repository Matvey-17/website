from django.contrib import admin
from django.contrib.admin import ModelAdmin

# Register your models here.


from products.models import ProductCategory, Product, Basket

admin.site.register(Basket)


class RecipeProductInline(admin.TabularInline):
    model = Product
    list_display = ['name']
    extra = 1


@admin.register(ProductCategory)
class Category(ModelAdmin):
    inlines = (RecipeProductInline,)
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
