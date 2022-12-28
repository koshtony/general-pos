from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

# form for user registrations
class UserRegForm(UserCreationForm):
    email= forms.EmailField(required=True)
    
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        
# form for user credentials updates

class UserUpdate(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User 
        fields = ['username','email']
        
class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','first','surname','phone','activation']