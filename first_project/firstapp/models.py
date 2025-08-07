from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from datetime import datetime
# Create your models here.
class Shops(models.Model):
    shop_id = models.AutoField(primary_key=True)
    shop_auth = models.ManyToManyField(User)
    shop_name =  models.CharField(max_length=100)
    shop_cat = models.CharField(max_length=100)
    shop_loc = models.CharField(max_length=100)
    shop_terms = models.TextField(max_length=1000,null=True,blank=True)
    shop_created = models.DateTimeField(default= timezone.now)
    
    
    def __str__(self):
        return self.shop_name
    
    def get_absolute_url(self):
        return reverse('firstapp-shops')
    
    class Meta:
        
        verbose_name_plural= "Shops"
    
class Stocks(models.Model):
    p_id=models.AutoField(primary_key=True)
    p_gen = models.BigIntegerField(default=hash(timezone.now))
    p_serial = models.CharField(max_length=100,default='No serial')
    p_name=models.CharField(max_length=100)
    p_category=models.CharField(max_length=100)
    p_desc=models.TextField()
    p_image=models.ImageField(default = 'product.jpg' , upload_to='stocks_images')
    p_qty=models.IntegerField()
    p_price=models.FloatField()
    p_cost=models.FloatField()
    p_vat = models.FloatField(default=0.0)
    p_disc = models.FloatField(default=0.0)
    p_shop = models.ForeignKey(Shops,on_delete=models.PROTECT)
    p_creator=models.ForeignKey(User,on_delete=models.PROTECT)
    p_created=models.DateTimeField(default= timezone.now)
    
    
    
    def __int__(self):
        return self.p_id
    
    def get_absolute_url(self):
        try:
            return reverse('firstapp-addstocks',kwargs={'pk':self.pk})
        except:
            return reverse('firstapp-stocks')
        
    class Meta:
        
        verbose_name_plural= "Stocks"

class Cart(models.Model):
    
    cart_stock = models.ForeignKey(Stocks,null=True,on_delete=models.SET_NULL)
    qty = models.FloatField(default=1.0,null=True)
    adjust_price = models.FloatField(default=0.0,null=True)
    initial_price = models.FloatField(default=0.0,null=True)
    price = models.FloatField(default=0.0,null=True)
    order_code = models.CharField(max_length=100,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,null=True)
    status = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.cart_stock.p_name
class Sales(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_serial = models.CharField(max_length=100)
    s_order_code = models.CharField(max_length=100,null=True,blank=True)
    s_name = models.CharField(max_length=100)
    s_shop = models.CharField(max_length=100)
    s_qty = models.FloatField()
    s_price = models.FloatField()
    s_cost = models.FloatField()
    s_negatives = models.FloatField()
    s_profit = models.FloatField()
    s_type = models.CharField(max_length=100,default="cash")
    s_status = models.CharField(max_length=100,default="sold")
    s_shop = models.ForeignKey(Shops,on_delete=models.PROTECT,null=True)
    s_created = models.DateTimeField(default= timezone.now)
    s_creator = models.ForeignKey(User,on_delete=models.PROTECT)
    
    def __str__(self):
        return self.s_name
    
    class Meta:
        
        verbose_name_plural= "Sales"
        
class Invoices(models.Model):
    i_id = models.AutoField(primary_key=True)
    i_code = models.CharField(max_length=100)
    i_serial = models.CharField(max_length=100)
    i_name = models.CharField(max_length=100)
    i_shop = models.CharField(max_length=100)
    i_qty = models.FloatField()
    i_price = models.FloatField()
    i_cost = models.FloatField()
    i_discount = models.FloatField()
    i_profit = models.FloatField()
    i_type = models.CharField(max_length=100)
    i_status = models.CharField(max_length=100)
    i_shop = models.ForeignKey(Shops,on_delete=models.PROTECT,null=True)
    i_created = models.DateTimeField(default= timezone.now)
    i_creator = models.ForeignKey(User,on_delete=models.PROTECT)
    
    def __str__(self):
        return self.i_name
    
    class Meta:
        
        verbose_name_plural= "Invoices"

class Paid(models.Model):

    sn = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    qty = models.FloatField()
    amount = models.FloatField()
    profit = models.FloatField()
    pay_type = models.CharField(max_length=100)
    waiter = models.ForeignKey(User,on_delete=models.PROTECT)
    date = models.DateTimeField(default= timezone.now)

    def __str__(self):

        return self.product
    
    class Meta:
        verbose_name_plural= "Paid Products"
    
class mpesaPay(models.Model):
    trans_id = models.CharField(max_length=100,default="")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100,default="")
    ref_no = models.CharField(max_length=100,default="")
    amount = models.CharField(max_length=100,default="")
    date = models.DateTimeField(default=timezone.now)
    details = models.TextField()

    def __str__(self):

        return self.name
    
    class Meta:
        
        verbose_name_plural= "Mpesa Payments"


    
class Expenses(models.Model):
    exp_id = models.AutoField(primary_key=True)
    exp_desc = models.TextField()
    exp_amount= models.FloatField()
    exp_creator = models.ForeignKey(User,on_delete=models.PROTECT)
    exp_shop = models.CharField(max_length=100,default=" ")
    exp_date = models.DateTimeField(default= timezone.now)
    
    def __str__(self):
        return self.exp_desc
    
    class Meta:
        
        verbose_name_plural = "Expenses"
    
class Transfers(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_serial = models.CharField(max_length=100)
    t_name = models.CharField(max_length=100)
    t_from = models.CharField(max_length=100)
    t_to =  models.CharField(max_length=100)
    t_qty = models.IntegerField()
    t_creator = models.ForeignKey(User,on_delete=models.PROTECT)
    t_created = models.DateTimeField(default= timezone.now)
    
    def __str__(self):
        return self.t_name
    class Meta:
        verbose_name_plural= "Transfers"

class Location(models.Model):
    loc_id = models.AutoField(primary_key=True)
    latitude = models.CharField(max_length = 100000)
    longitude = models.CharField(max_length = 100000,default=0.0)
    loc_tag = models.CharField(max_length=100,default="not set")
    loc_creator = models.ForeignKey(User,on_delete=models.CASCADE)
    loc_created = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return f"latitude:{self.latitude} longitude:{self.longitude}"

class Tasks(models.Model):

    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=1000)
    task_desc = models.TextField()
    task_to = models.ManyToManyField(User)
    task_status = models.CharField(max_length=1000)
    task_creator = models.CharField(max_length=1000)
    task_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.task_name
    
    class Meta:
        
        verbose_name_plural= "Tasks"
    
    
class Debts(models.Model):
    
    debt_id = models.AutoField(primary_key=True)
    debt_cus = models.CharField(max_length=1000)
    debt_amnt = models.FloatField(default=0.0)
    debt_rem = models.FloatField(default=0.0)
    debt_last = models.DateTimeField(default=timezone.now)
    debt_remks = models.TextField()
    debt_creator = models.ForeignKey(User,on_delete=models.PROTECT)
    
    def __str__(self):
        return self.debt_cus
    
    class Meta:
        
        verbose_name_plural = "Debt List"

class Contacts(models.Model):
    
    cont_id = models.AutoField(primary_key=True)
    cont_name = models.CharField(max_length=100)
    cont_phone = models.CharField(max_length=100)
    cont_created = models.DateTimeField(default=timezone.now)
    
    
    class Meta:
        
        verbose_name_plural= "Customer Contacts"
        
        
class Organisation(models.Model):
    
    org_id = models.AutoField(primary_key=True)
    org_name = models.CharField(max_length=100)
    org_details = models.TextField()
    org_creator = models.ForeignKey(User,on_delete=models.PROTECT)
    org_created = models.DateTimeField(default=timezone.now)
    org_summary_notes = models.TextField(null=True,blank=True)
    logo = models.ImageField(default = 'product.jpg' , upload_to='orgs_images')
    
    
    
    class Meta:
        
        verbose_name_plural= "Organisation"
        
        
class Customers(models.Model):
    
    cus_id = models.AutoField(primary_key=True)
    cus_name = models.CharField(max_length=100)
    cus_phone = models.CharField(max_length=100)
    cus_email = models.CharField(max_length=100)
    cus_address = models.CharField(max_length=100)
    cus_details = models.TextField()
    cus_creator = models.ForeignKey(User,on_delete=models.PROTECT)
    cus_created = models.DateTimeField(default=timezone.now)
    
    cus_ref_code = models.CharField(max_length=100,null=True,blank=True)  
    
    def __str__(self):
        return self.cus_name 
    
    class Meta:
        
        verbose_name_plural= "Customers"