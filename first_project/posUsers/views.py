from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegForm
# Create your views here.

def register(request):
    form=UserRegForm()
    if request.method=='POST':
        form=UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get("username")
            messages.success(request,f'{username} account created')
            return redirect('login')
    return render(request,'posUsers/register.html',{'form':form})
    
@login_required   
def profile(request):
    return render(request,'posUsers/profile.html')