from django.contrib import admin
from ecomapp.models import Product


# Register your models here.
#admin.site.register(Product)

class productAdmin(admin.ModelAdmin):
    list_display=['name','price','cat','is_active']
    list_filter=['cat','is_active']

admin.site.register(Product,productAdmin)