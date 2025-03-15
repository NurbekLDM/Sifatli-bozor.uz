from django.db import models
from django.core.exceptions import ValidationError
import re
from django.utils import timezone

# Validation for Uzbekistan phone numbers
def validate_uzbekistan_phone(value):
    # Expected format: +998 (XX) XXX-XX-XX
    pattern = re.compile(r'^\+998 \(\d{2}\) \d{3}-\d{2}-\d{2}$')
    if not pattern.match(value):
        raise ValidationError(
            'Telefon raqami quyidagi formatda bo\'lishi kerak: +998 (XX) XXX-XX-XX',
            code='invalid_phone'
        )

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategoriya nomi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        permissions = [
            ("view_categories", "Can view categories"),
        ]

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Mahsulot nomi")
    description = models.TextField(verbose_name="Tavsif")
    price = models.DecimalField(
        max_digits=20,
        decimal_places=0,
        verbose_name="Narx",
        help_text="Narx so'mda kiritiladi"
    )
    image = models.ImageField(
        upload_to='product_images/',
        blank=True,
        null=True,
        verbose_name="Rasm"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Yaratilgan sana"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Kategoriya"
    )

    def __str__(self):
        return self.name

    def image_url(self):
        # Check if image exists and return its URL, otherwise return a default
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/images/default_product_image.jpg'  # Ensure this path exists in your static files

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']  # Sort by creation date (newest first)
        permissions = [
            ("view_products", "Can view products"),
        ]

class HeroImage(models.Model):
    image = models.ImageField(
        upload_to='hero_images/',
        blank=True,
        null=True,
        verbose_name="Rasm"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Tavsif"
    )

    def __str__(self):
        return self.description if self.description else "Hero Image"

    class Meta:
        verbose_name = "Hero Rasm"
        verbose_name_plural = "Hero Rasmlar"

class Inquiry(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='inquiries',
        verbose_name="Mahsulot"
    )
    name = models.CharField(max_length=100, verbose_name="Ism")
    surname = models.CharField(max_length=100, verbose_name="Familiya")
    phone = models.CharField(
        max_length=18,
        validators=[validate_uzbekistan_phone],
        verbose_name="Telefon raqami",
        help_text="Format: +998 (XX) XXX-XX-XX"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Yaratilgan sana"
    )

    def __str__(self):
        return f"{self.product.name} uchun so'rov - {self.name} {self.surname}"

    def product_image_url(self):
        return self.product.image_url()

    class Meta:
        verbose_name = "So'rov"
        verbose_name_plural = "So'rovlar"
        ordering = ['-created_at']
        permissions = [
            ("view_inquiries", "Can view inquiries")
        ]