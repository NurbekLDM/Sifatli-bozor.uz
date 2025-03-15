from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProductSitemap, StaticViewSitemap
from . import views
from django.contrib.auth.views import LogoutView

sitemaps = {
    'products': ProductSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('admin-panel/hero/add/', views.hero_image_add, name='hero_image_add'),
    path('admin-panel/hero/<int:hero_id>/edit/', views.hero_image_edit, name='hero_image_edit'),
    path('admin-panel/hero/<int:hero_id>/delete/', views.hero_image_delete, name='hero_image_delete'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('admin-panel/product/add/', views.product_add, name='product_add'),
    path('admin-panel/product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('admin-panel/product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('admin-panel/category/add/', views.category_add, name='category_add'),
    path('admin-panel/category/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('admin-panel/category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('admin-panel/add-user/', views.add_user, name='add_user'),
    path('admin-panel/user/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('admin-panel/user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('login/admin_panel/', views.admin_panel, name='admin_panel'),
    path('', views.homePage, name='homePage'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]