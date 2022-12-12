from django.shortcuts import render
from django.http import HttpResponse
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
    return render(request,'firstapp/counter.html')