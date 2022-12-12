from django.shortcuts import render
from django.http import HttpResponse
from .models import Stocks
# Create your views here.
orders = [
    {
        'title':"today orders",
        'qty':10
    },
    
]
def home(request):
    data={
        "orders":orders
    }
    return render(request,'firstapp/home.html',data)

def counter(request):
    stocks = {
        'products': Stocks.objects.all()
    }
    return render(request,'firstapp/counter.html',stocks)