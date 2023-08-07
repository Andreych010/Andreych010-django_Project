from django.contrib import admin

from blog.models import BlogPost
from catalog.models import Product, Category, Version


# admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'name', 'purchase_price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'number_version', 'name_version', 'active_version',)
    list_filter = ('active_version',)
    search_fields = ('number_version',)

@admin.register(BlogPost)
class BlogPost(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'body', 'preview', 'date_creation', 'sign_publication', 'number_views',)
    search_fields = ('title',)

