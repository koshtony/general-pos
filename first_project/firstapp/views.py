from django.shortcuts import render
from django.views.generic import ListView,CreateView
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

class StocksListViews(ListView):
    model = Stocks
    template_name = 'firstapp/stocks.html'
    context_object_name = 'products'
    
class StocksCreateView(CreateView):
    model = Stocks
    template_name = 'firstapp/add_stocks.html'
    fields = ['p_name','p_category','p_desc',
              'p_image','p_qty','p_price','p_cost','p_created'
              ]
    
    def form_valid(self,form):
        form.instance.p_creator = self.request.user
        return super().form_valid(form)
