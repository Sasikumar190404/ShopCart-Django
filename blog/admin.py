from django.contrib import admin
from .models import *
# Register your models here.

class Category_admin(admin.ModelAdmin):
    list_display = ("name","image","description")

admin.site.register(Category,Category_admin)
admin.site.register(Product)