from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register,name='posUsers-register'),
    path('profile/', views.profile,name='posUsers-profile')
    
    
]