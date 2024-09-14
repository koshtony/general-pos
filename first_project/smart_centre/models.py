from django.db import models
from django.utils import timezone
from datetime import datetime


# Create your models here.

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
    products_rdp = models.FloatField()
    product_rrp = models.FloatField()
    product_wholesale_price = models.FloatField(null=True)
    retail = models.BooleanField(default=True)
    launch = models.DateField(default=timezone.now)
    eol_date = models.DateTimeField(default = datetime.now()+ datetime.timedelta(days=6*30) )
    
    product_image = models.ImageField(default="product.jpg",upload_to="smart_products")
    
    def __str__(self):
        
        return self.product_name + "\n"+ "STORAGE: "+self.product_rom + "\n" \
    + "MEMORY: "+self.product_ram + "\n" + "Camera: "+self.product_camera + "\n" + "BATTERY: "+self.product_battery + "\n" \
        + "PROCESSOR: "+self.product_processor + "\n" + "OS: "+self.product_os + "\n" + "CONNECTIVITY: "+self.product_connectivity + "\n" \
        + "COLORS: "+self.product_colors
    
class StocksList(models.Model):
    
    device_id = models
    
    