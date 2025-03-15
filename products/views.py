from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required , permission_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product, Inquiry, Category, HeroImage
from django.db.models import Q  
from .forms import ProductForm, InquiryForm, CategoryForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User, Group , Permission
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST



class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


def homePage(request):
    hero_image = HeroImage.objects.first()
    latest_products = Product.objects.order_by('-created_at')[:3]
    return render(request, 'products/home.html', {
        'hero_image': hero_image,
        'latest_products': latest_products,
    })

@login_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')  # New field
        last_name = request.POST.get('last_name')   # New field
        group_name = request.POST.get('group')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi allaqachon mavjud.")
            return redirect('admin_panel')

        # Create the user with is_staff=True
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,  # Add first name
            last_name=last_name,    # Add last name
            is_staff=True
        )

        # Assign the user to the "order_admin" group
        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except Group.DoesNotExist:
            messages.error(request, f"{group_name} guruhi topilmadi.")
            user.delete()  # Rollback user creation if group doesn't exist
            return redirect('admin_panel')

        # Automatically assign the "Can view inquiries" permission
        try:
            content_type = ContentType.objects.get_for_model(Inquiry)
            permission = Permission.objects.get(codename='view_inquiries', content_type=content_type)
            user.user_permissions.add(permission)
            messages.success(request, f"{username} muvaffaqiyatli qo'shildi, {group_name} guruhiga biriktirildi va 'Can view inquiries' ruxsati berildi.")
        except Permission.DoesNotExist:
            messages.error(request, "'Can view inquiries' ruxsati topilmadi. Iltimos, admin paneldan tekshiring.")
            return redirect('admin_panel')

        return redirect('admin_panel')

    return redirect('admin_panel')


@login_required
def admin_panel(request):
    # Existing code to fetch products, inquiries, categories
    products = Product.objects.all()  # Replace with your model
    inquiries = Inquiry.objects.all()  # Replace with your model
    categories = Category.objects.all()  # Replace with your model
    users = User.objects.all()  # Fetch all users to display in the table
    hero_image = HeroImage.objects.first()
    user_permissions = request.user.get_all_permissions()
    return render(request, 'products/admin_panel.html', {
        'products': products,
        'inquiries': inquiries,
        'categories': categories,
        'users': users,
        'hero_image': hero_image,
         'user_permissions': user_permissions,
        'is_superuser': request.user.is_superuser,
    })
    

@require_POST
@login_required
def hero_image_add(request):
    if request.user.is_superuser:
        image = request.FILES.get('image')
        if image:
            HeroImage.objects.all().delete()  # Only one hero image allowed
            HeroImage.objects.create(image=image)
    return redirect('admin_panel')

@login_required
@permission_required('products.change_heroimage', raise_exception=True)
def hero_image_edit(request, hero_id):
    hero_image = get_object_or_404(HeroImage, id=hero_id)
    if request.method == 'POST':
        if request.FILES.get('image'):
            hero_image.image = request.FILES['image']
            hero_image.save()
        return redirect('admin_panel')
    return render(request, 'products/admin_panel.html', {'hero_image': hero_image})

@login_required
@permission_required('products.delete_heroimage', raise_exception=True)
def hero_image_delete(request, hero_id):
    hero_image = get_object_or_404(HeroImage, id=hero_id)
    if request.method == 'POST':
        hero_image.delete()
        return redirect('admin_panel')
    return render(request, 'products/admin_panel.html', {'hero_image': hero_image})
    
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')  # New field
        last_name = request.POST.get('last_name')    # New field

        # Check if username is already taken by another user
        if username != user.username and User.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi allaqachon mavjud.")
            return redirect('admin_panel')

        # Update user details
        user.username = username
        user.email = email
        user.first_name = first_name  # Update first name
        user.last_name = last_name    # Update last name
        if password:  # Only update password if provided
            user.set_password(password)
        user.save()

        messages.success(request, f"{username} muvaffaqiyatli tahrirlandi.")
        return redirect('admin_panel')

    return redirect('admin_panel')

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        # Prevent deleting the current user (optional)
        if user == request.user:
            messages.error(request, "Siz o'zingizni o'chira olmaysiz!")
            return redirect('admin_panel')

        username = user.username
        user.delete()
        messages.success(request, f"{username} muvaffaqiyatli o'chirildi.")
        return redirect('admin_panel')

    return redirect('admin_panel')

@login_required
@staff_member_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Mahsulot muvaffaqiyatli qo'shildi!")
            return redirect('admin_panel')
        else:
            # Show error message only if form validation fails
            messages.error(request, "Mahsulot qo'shishda xatolik! Iltimos, barcha maydonlarni to'g'ri to'ldiring.")
    else:

        form = ProductForm()

    return render(request, 'products/product_form.html', {'form': form, 'categories': Category.objects.all()})

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
            
            # Add success message
            messages.success(request, "Buyurtmangiz muvaffaqiyatli yuborildi!")
            return redirect('product_detail', pk=product.pk)
        else:
            # Add error message if form is invalid
            messages.error(request, "Buyurtma yuborilmadi. Iltimos ma'lumotlarni to'g'ri kiriting.")
    else:
        form = InquiryForm()
    return render(request, 'products/product_detail.html', {'product': product, 'form': form})


def product_list(request):
    query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')
    sort = request.GET.get('sort', '')

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if selected_category:
        products = products.filter(category_id=selected_category)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    categories = Category.objects.all()

    for product in products:
        if not product.image:
            product.image_url = '/static/images/default_product_image.jpg'

    return render(request, 'products/product_list.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': selected_category,
        'sort': sort,
    })



