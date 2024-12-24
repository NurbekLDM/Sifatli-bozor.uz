from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin 

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('admin-panel/product/add/', views.product_add, name='product_add'),
    path('admin-panel/product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('admin-panel/product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('admin-panel/category/add/', views.category_add, name='category_add'),
    path('admin-panel/category/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('admin-panel/category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls, name='admin_panel'),
]