from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegForm,UserUpdate,ProfileUpdate
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
    user_form = UserUpdate(instance=request.user)
    profile_form = ProfileUpdate(instance=request.user.profile)
    forms = {
            'user_form':user_form,
            'profile_form':profile_form
        }
    if request.method == 'POST':
        user_form = UserUpdate(request.POST,instance=request.user)
        profile_form = ProfileUpdate(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,f'{request.user} profile updated')
            return redirect('posUsers-profile')
        
    return render(request,'posUsers/profile.html',forms)