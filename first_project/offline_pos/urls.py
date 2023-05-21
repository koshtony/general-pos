from django.urls import path
from . import views
from .views import offline_counter,feeds_indexDB
urlpatterns = [
    path('offline-counter', views.offline_counter,name='offline-counter'),
    path('feeds_stocksDB', views.feeds_indexDB,name='offline-stocksDB'),
    
]