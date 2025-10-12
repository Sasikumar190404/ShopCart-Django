from django.db import models
from django.contrib.auth.models import User
import datetime
import os

# Function to rename uploaded files
def get_filename(request, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{now_time}_{filename}"
    return os.path.join('uploads/', new_filename)

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=get_filename, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show, 1-hidden")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name  # This ensures proper display in admin & dropdowns

# Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # lowercase field name
    name = models.CharField(max_length=150, null=False, blank=False)
    vendor = models.CharField(max_length=150, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(max_length= 10 ,null=False, blank=False)
    selling_price = models.FloatField(max_length=10,null=False, blank=False)
    product_image = models.ImageField(upload_to=get_filename, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show, 1-hidden")
    trending = models.BooleanField(default=False, help_text="0-default, 1-trending")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name  # This ensures proper display in admin

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_cost(self):
        return self.product_qty*self.product.selling_price
    
class Favourites(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)