from django.db import models
from django.core.exceptions import ValidationError
import re

def validate_uzbekistan_phone(value):
    pattern = re.compile(r'^\+998 \(\d{2}\) \d{3}-\d{2}-\d{2}$')
    if not pattern.match(value):
        raise ValidationError('Phone number must be in the format: +998 (XX) XXX-XX-XX')

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    def __str__(self):
        return self.name

class Inquiry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=18)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry for {self.product.name}"