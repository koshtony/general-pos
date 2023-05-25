from django.urls import path
from . import views
from .views import offline_counter,offline_sales,commit_sales,feeds_indexDB
urlpatterns = [
    path('offline-counter', views.offline_counter,name='offline-counter'),
    path('offline-sales', views.offline_sales,name='offline-sales'),
    path('commit-sales', views.commit_sales,name='commit-sales'),
    path('feeds_stocksDB', views.feeds_indexDB,name='offline-stocksDB'),
    
]