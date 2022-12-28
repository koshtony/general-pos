from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_images')
    first = models.CharField(max_length=50,default="None")
    surname = models.CharField(max_length=50,default="None")
    phone = models.CharField(max_length=20,default="None")
    activation = models.CharField(max_length=20,default="None")
    
    
    def __str__(self):
        return f'{self.user.username} Profile'

