from django.contrib import admin
from .models import Product, Inquiry, Category, HeroImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'category', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50">'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Rasm'

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'surname', 'phone', 'created_at')

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ('description', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50">'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Rasm'

    class Meta:
        verbose_name = 'Qahramon Rasm'
        verbose_name_plural = 'Qahramon Rasmlar'