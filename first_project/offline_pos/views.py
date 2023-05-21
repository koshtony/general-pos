from django.shortcuts import render
from firstapp.models import Stocks
from django.http import JsonResponse,HttpResponse
from django.core import serializers
# handles offline counter
def offline_counter(request):
    
    return render(request,'offline_pos/off_counter.html')

# 
def feeds_indexDB(request):

    products = Stocks.objects.all()
    products_json = serializers.serialize('json',products)
    return HttpResponse(products_json)
