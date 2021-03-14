# Django:
from django.contrib import admin

# Localfolder:
from .models import Category, CategoryKeyword


# Register application 'Category' in admin-panel
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "description", "is_default")
    list_filter = ("mcc_code", "owner")
    search_fields = ("category_name",)


# Register application 'CategoryKeyword' in admin-panel
@admin.register(CategoryKeyword)
class CategoryKeywordAdmin(admin.ModelAdmin):
    list_display = ("word", "category")
    list_filter = ("word", "category")
    search_fields = ("word",)
