from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here.
class Contacts(models.Model):

    current_user = models.CharField(max_length=100,default=" ")
    contact_mode = models.CharField(choices= (('file','file'),('single','single')),default='single',max_length=100)
    contact_name =  models.CharField(max_length=100,default=" ")
    contact_number = models.CharField(max_length=100,default=" ")
    contact_date = models.DateTimeField(default=timezone.now)
    contact_file = models.FileField(default='contacts.xlsx',upload_to='contact_files')

class SentRecord(models.Model):
    
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    message = RichTextField()
    cost = models.FloatField()
    sent_date = models.DateTimeField(default=timezone.now)
    creator = models.CharField(max_length=100,default="koshtech")

class Settings(models.Model):

    this_user = models.CharField(max_length=100)
    wallet = models.FloatField()
    limit = models.FloatField(default=1000.0)
    current = models.FloatField(default=0.0)