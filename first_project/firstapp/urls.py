from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='firstapp-home'),
    path('counter/', views.counter,name='firstapp-counter')
]