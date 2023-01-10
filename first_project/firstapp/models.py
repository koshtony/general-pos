from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class Shops(models.Model):
    shop_id = models.AutoField(primary_key=True)
    shop_auth = models.ManyToManyField(User)
    shop_name =  models.CharField(max_length=100)
    shop_cat = models.CharField(max_length=100)
    shop_loc = models.CharField(max_length=100)
    shop_created = models.DateTimeField(default= timezone.now())
    
    
    def __str__(self):
        return self.shop_name
    
    def get_absolute_url(self):
        return reverse('firstapp-shops')
    
class Stocks(models.Model):
    p_id=models.AutoField(primary_key=True)
    p_serial = models.CharField(max_length=100,default='No serial')
    p_name=models.CharField(max_length=100)
    p_category=models.CharField(max_length=100)
    p_desc=models.TextField()
    p_image=models.ImageField(default = 'product.jpg' , upload_to='stocks_images')
    p_qty=models.IntegerField()
    p_price=models.FloatField()
    p_cost=models.FloatField()
    p_shop = models.ForeignKey(Shops,on_delete=models.PROTECT)
    p_creator=models.ForeignKey(User,on_delete=models.PROTECT)
    p_created=models.DateTimeField(default= timezone.now())
    
    
    
    def __int__(self):
        return self.p_id
    
    def get_absolute_url(self):
        try:
            return reverse('firstapp-updatestocks',kwargs={'pk':self.pk})
        except:
            return reverse('firstapp-stocks')

class Sales(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_serial = models.CharField(max_length=100)
    s_name = models.CharField(max_length=100)
    s_shop = models.CharField(max_length=100)
    s_price = models.FloatField()
    s_cost = models.FloatField()
    s_negatives = models.FloatField()
    s_profit = models.FloatField()
    s_shop = models.ForeignKey(Shops,on_delete=models.PROTECT)
    s_created = models.DateTimeField(default= timezone.now())
    s_creator = models.ForeignKey(User,on_delete=models.PROTECT)
    
    def __str__(self):
        return self.s_name
    
class Expenses(models.Model):
    exp_id = models.AutoField(primary_key=True)
    exp_desc = models.TextField()
    exp_amount= models.FloatField()
    exp_creator = models.ForeignKey(User,on_delete=models.PROTECT)
    exp_shop = models.ForeignKey(Shops,on_delete=models.PROTECT)
    exp_date = models.DateTimeField(default= timezone.now())
    
    def __str__(self):
        return self.exp_desc
    
class Transfers(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_serial = models.CharField(max_length=100)
    t_name = models.CharField(max_length=100)
    t_from = models.CharField(max_length=100)
    t_to =  models.CharField(max_length=100)
    t_qty = models.IntegerField()
    t_creator = models.ForeignKey(User,on_delete=models.PROTECT)
    t_created = models.DateTimeField(default= timezone.now())
    
    def __str__(self):
        return self.t_name
