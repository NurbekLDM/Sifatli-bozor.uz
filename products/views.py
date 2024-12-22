from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product, Inquiry, Category
from django.db.models import Q  
from .forms import ProductForm, InquiryForm, CategoryForm



@login_required
@staff_member_required
def admin_panel(request):
    products = Product.objects.all()
    inquiries = Inquiry.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/admin_panel.html', {
        'products': products,
        'inquiries': inquiries,
        'categories': categories,
    })

@login_required
@staff_member_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

@login_required
@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

@login_required
@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_panel')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

@login_required
@staff_member_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = CategoryForm()
    return render(request, 'products/category_form.html', {'form': form})

@login_required
@staff_member_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/category_form.html', {'form': form})

@login_required
@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('admin_panel')
    return render(request, 'products/category_confirm_delete.html', {'category': category})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.product = product
            inquiry.save()


            return redirect('product_detail', pk=product.pk)
    else:
        form = InquiryForm()
    return render(request, 'products/product_detail.html', {'product': product, 'form': form})




def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    return render(request, 'products/product_list.html', {'products': products, 'query': query})
    redirect('product_list')
