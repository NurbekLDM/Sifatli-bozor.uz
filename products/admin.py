from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Product, Inquiry, Category, HeroImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'category', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50">'
        return "No Image"
    
    image_preview.allow_tags = True
    image_preview.short_description = 'Rasm'

admin.site.register(Product, ProductAdmin)


class InquiryAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'surname', 'phone', 'created_at')

    def has_add_permission(self, request):
        # Faqat superuser qo'sha oladi
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        # Faqat superuser o'zgartira oladi
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # Faqat superuser o'chira oladi
        return request.user.is_superuser

admin.site.register(Inquiry, InquiryAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)

class HeroImageAdmin(admin.ModelAdmin):
    list_display = ('description', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50">'
        return "No Image"
    
    image_preview.allow_tags = True
    image_preview.short_description = 'Rasm'

admin.site.register(HeroImage, HeroImageAdmin)
