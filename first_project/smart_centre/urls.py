from django.urls import path 
from . import views 
from .views import stocks_upload,sales_summary

urlpatterns = [

    path('stocks_upload/', stocks_upload, name='smart-stocks-upload'),
    path('sales-summary/', sales_summary, name='smart-sales-summary'),
]