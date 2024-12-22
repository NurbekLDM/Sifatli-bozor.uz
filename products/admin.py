from django.contrib import admin
from .models import Product, Inquiry , Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'category','image_preview')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50">'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image'

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'surname', 'phone', 'created_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)