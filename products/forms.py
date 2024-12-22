from django import forms
from .models import Product, Inquiry, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'surname', 'phone']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']