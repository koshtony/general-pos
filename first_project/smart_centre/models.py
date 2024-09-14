from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


# Create your models here.


class Specifications(models.Model):
    
    product_rom = models.CharField(max_length=100,choices=(
        ("16GB","16GB"),("32GB","32GB"),("64GB","64GB"),("128GB","128GB"),("256GB","256GB"),("512GB","512GB"),("1TB","1TB")
        ))
    product_ram = models.CharField(max_length=100,choices=(
        ("16GB","16GB"),("32GB","32GB"),("64GB","64GB")))
    
    product_camera = models.TextField()
    product_battery = models.TextField()
    product_processor  = models.TextField()
    product_os = models.TextField()
    product_connectivity = models.TextField()
    product_colors = models.TextField()
    
    
    
    
#
class Brands(models.Model):
    
    brand_id = models.AutoField(primary_key=True)
    brand_name  = models.CharField(max_length=100)
    country = models.CharField(max_length=100,default="")
    
class Distributor(models.Model):
    
    distributor_id = models.AutoField(primary_key=True)
    distributor_name = models.CharField(max_length=100)
    distributor_address = models.TextField("")
    distributor_brands = models.ManyToManyField(Brands,related_name="brands_distributor")
    
    def __str__(self):
        
        return self.distributor_name

class ProductName(models.Model):
  
    product_name_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_brand = models.ForeignKey(Brands, null=True, on_delete=models.SET_NULL)
    product_sku = models.CharField(max_length=100)
    prodyuct_specs = models.TextField()
    products_rdp = models.FloatField()
    product_rrp = models.FloatField()
    product_wholesale_price = models.FloatField(null=True)
    retail = models.BooleanField(default=True)
    launch = models.DateField(default=timezone.now)
    eol_date = models.DateTimeField(default = datetime.datetime.now()+ datetime.timedelta(days=6*30) )
    
    product_image = models.ImageField(default="product.jpg",upload_to="smart_products")
    
    def __str__(self):
        
        return self.product_name + "\n"+self.products_specs
    
class StocksList(models.Model):
    
    device_id = models.AutoField(primary_key=True)
    device_serial1 = models.CharField(max_length=100)
    device_serial2 = models.CharField(max_length=100)
    device_specs = models.ForeignKey(ProductName, related_name="product_specs",null=True,on_delete=models.SET_NULL)
    device_stock_date = models.DateTimeField(default=timezone.now)
    device_added_by = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    device_stock_stage = models.CharField(max_length=100,default="Distributor",choices=(("Distributor","Distributor"),("Retailer","Retailer")))
    
    
class DeviceSales(models.Model):
    
    
    device_sale_id = models.AutoField(primary_key=True)
    device_product_spec = models.ForeignKey(StocksList, null=True ,on_delete=models.SET_NULL)
    
    profit = models.FloatField()
    stage = models.CharField(max_length=100,choices=(("cart","cart"),("sold","sold"),("disputed","disputed"),("returned","returned")))
    sales_date = models.DateField(default=timezone.now(),verbose_name="Sales Date")
    disputed_date = models.DateField(null=True,verbose_name="Disputed Date")
    returned_date = models.DateField(null=True,verbose_name="Returned Date")
    sold_by = models.ForeignKey(User,null=True,on_delete=models.SET_NULL, verbose_name="Sales Man")
    
    # customer details
    
    customer_name = models.CharField(max_length=100)
    customer_id = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=100)
    customer_address = models.TextField()
    warranty = models.ImageField(default="warranty.jpg",upload_to="smart_products_warranty")
    warranty_expiry_date = models.DateTimeField(null=True)
    
    
    
    
    