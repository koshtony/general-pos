from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Stocks(models.Model):
    p_id=models.IntegerField(primary_key=True)
    p_name=models.CharField(max_length=100)
    p_category=models.CharField(max_length=100)
    p_desc=models.TextField()
    p_image=models.CharField(max_length=1000)
    p_qty=models.IntegerField()
    p_price=models.FloatField()
    p_cost=models.FloatField()
    p_created=models.DateTimeField()
    p_creator=models.ForeignKey(User,on_delete=models.PROTECT)
    
    def __str__(self):
        return self.p_name
    