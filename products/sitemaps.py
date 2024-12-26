from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Product

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ['homePage', 'product_list']

    def location(self, item):
        return reverse(item)
