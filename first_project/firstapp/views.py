from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import ListView,CreateView,UpdateView,DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.templatetags.static import static
from django.utils.decorators import method_decorator
from django.core import serializers
from .models import Stocks,Shops,Sales,Expenses
from datetime import datetime
import json
import time
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
    sums = 0
    if 'sales' in request.session:
        for key,value in request.session["sales"].items():
            sums+=float(request.session["sales"][key]["price"])
            
  
    stocks = {
        'products': Stocks.objects.all(),
        'sum':sums
        
    }
    return render(request,'firstapp/counter.html',stocks)

def Charts(request):
    
    x_sales = []
    y_sales = []
    
    sales  = Sales.objects.values('s_name').annotate(total_profit= Sum('s_profit'))
    for sale in sales:
        x_sales.append(sale["s_name"])
        y_sales.append(sale["total_profit"])
    print(x_sales)
    contxt = {
        "labels": x_sales,
        "data":y_sales,
    }
    return render(request,'firstapp/reports.html',contxt)

# gets the select item info 
def getCounter(request):
    pid = request.GET.get("pid")
    qty = request.GET.get("qty")
    product = Stocks.objects.get(p_id=pid)
    name  = product.p_name
    serial = product.p_serial
    cat =product.p_category
    shops = product.p_shop.shop_id
    price = product.p_price
    cost = product.p_cost
    total = float(price)*int(qty)
    total_cost = float(cost)*int(qty) 
    profit = total-total_cost
    pid = hash(time.time())+int(pid)
    data ={pid:
        
            {
                "serial":serial,"name":name,"category":cat,"shops":shops,
                "qty":qty,"price1":price,"price":total,"cost":total_cost,
                "profit":profit
                
            }
                
        }
    
    

    if request.session.has_key('sales'):
        if pid not in request.session["sales"]:
            request.session["sales"] = dict(list(request.session["sales"].items())+ list(data.items()))
       
    else:
        request.session["sales"] = data
            
    
        
    pass_data = {"name":request.session["sales"][pid]["name"],
                 
                 "qty":request.session["sales"][pid]["qty"],
                 
                 "price":request.session["sales"][pid]["price1"],
                 
                 "total":request.session["sales"][pid]["price"]
                 
                }
       
    filt_data = Stocks.objects.filter(p_name=name).first()
    new_obj=Stocks.objects.get(p_name=name)
    new_obj.p_qty = filt_data.p_qty - int(qty)
    new_obj.save()
    return JsonResponse(pass_data,status=200)

def addSales(request):
    if 'sales' in request.session:
        for key,value in request.session["sales"].items():
            sales= Sales(
                s_serial = request.session["sales"][key]["serial"],
                s_name = request.session["sales"][key]["name"],
                s_shop = Shops.objects.get(shop_id=request.session["sales"][key]["shops"] ),
                s_price = request.session["sales"][key]["price"],
                s_cost = request.session["sales"][key]["cost"],
                s_negatives = 0,
                s_profit = request.session["sales"][key]["profit"],
                s_created = datetime.now(),
                s_creator = request.user
            )
            sales.save()
        del request.session["sales"]
        return redirect('firstapp-counter')
        

def stocksView(request): 
    products = Stocks.objects.all()        
    contxt = {
            'products':products,
    }
    return render(request,'firstapp/stocks.html',contxt)

def stocksPostView(request):
    if request.POST:
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        if date1!='' or date1!='':
            products = Stocks.objects.filter(p_created__gte=date1,p_created__lte=date2)
            products = serializers.serialize('json',products)
           
            
        else: 
            products = Stocks.objects.all().values()
            products = serializers.serialize('json',products)
        
        return JsonResponse(products,safe=False)
    
    
class StocksCreateView(CreateView):
    model = Stocks
    template_name = 'firstapp/add_stocks.html'
    fields = ['p_name','p_serial','p_category','p_desc',
              'p_image','p_qty','p_price','p_cost','p_shop','p_creator','p_created'
              ]
    
    def form_valid(self,form):
        form.instance.p_creator = self.request.user
        return super().form_valid(form)
    
class StocksDetailView(DetailView):
    model= Stocks

class StocksUpdateView(UpdateView):
    model = Stocks
    template_name = 'firstapp/update_stocks.html'
    fields = ['p_name','p_category','p_desc',
              'p_image','p_qty','p_price','p_cost','p_created'
              ]
    
    def form_valid(self,form):
        form.instance.p_creator = self.request.user
        return super().form_valid(form)
    
    
# display the shops details
class ShopsListView(ListView):
    model =Shops
    template_name = 'firstapp/shops_list.html'
    context_object_name = 'shops'
    paginate_by = 5
    

class ShopsCreateView(SuccessMessageMixin,CreateView):
    model = Shops
    template_name = 'firstapp/add_shops.html'
    success_message = ' shop added successfully'
    fields =['shop_name','shop_cat','shop_loc','shop_auth']
    
    def form_valid(self,form):
        return super().form_valid(form)
    
def shopsUpdate(request):
    if request.POST:
        id = request.POST.get("id")
        name = request.POST.get("name")
        cat = request.POST.get("cat")
        loc = request.POST.get("loc")
        data = {"id":id}
        filt_shop = Shops.objects.get(shop_id=id)
        filt_shop.shop_name = name
        filt_shop.shop_cat = cat
        filt_shop.shop_loc = loc
        filt_shop.save()
        return JsonResponse(data)
    
# ---- sales view

class SalesListView(ListView):
    model = Sales
    template = 'firstapp/sales_list.html'
    context_object_name = 'sales'
   
    
    def get_queryset(self):
        if self.request.GET:
            date1 = self.request.GET.get("date1")
            date2 = self.request.GET.get("date2")
            queryset =  Sales.objects.filter(s_created__gte=date1,s_created__lte=date2)
        
            return queryset
        return super().get_queryset()
    
def salesPostView(request):
    if request.POST:
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        if date1!='' or date1!='':
            sales = Sales.objects.filter(s_created__gte=date1,s_created__lte=date2)
            sales = serializers.serialize('json',sales)
           
            
        else: 
            sales = Sales.objects.all().values()
            sales = serializers.serialize('json',sales)
        
        return JsonResponse(sales,safe=False)
    
def OrdersView(request):
    return render(request, 'firstapp/orders_list.html')

def InvoiceView(request):
    data = request.GET.get("htmlData")
    if data != None:
        data = '<html>'+data + '</html>'
        html_path =  "/home/koshtech/Videos/general-pos/first_project/firstapp/static/firstapp/exports/invoice.html"
        with open(html_path,"w+") as file:
        
            file.write(data)
            
        
        
    return render(request,'firstapp/invoice.html')


def financeView(request):
    
    
    
    contxt = {
                  "expenses":Expenses.objects.all(),
                  "sum": Expenses.objects.aggregate(Sum("exp_amount"))["exp_amount__sum"],
                  "profit": Sales.objects.aggregate(Sum("s_profit"))["s_profit__sum"],
                  "net_profit": Sales.objects.aggregate(Sum("s_profit"))["s_profit__sum"]-Expenses.objects.aggregate(Sum("exp_amount"))["exp_amount__sum"] 
              
              }
    return render(request,'firstapp/financials.html',contxt)

def financePostView(request):
   
        date = request.GET.get("date")
        desc = request.GET.get("desc")
        amount = request.GET.get("amount")
        print(desc)
        exp = Expenses(exp_desc = desc,exp_amount = amount , 
                       exp_date = date, exp_creator=request.user
                       )
        exp.save()
        
        return JsonResponse({'date':date,desc:"desc","amount":amount})
    
#==========handles post requests from expenses page ======
   
def financeUpdateView(request):
    if request.POST:
        id = request.POST.get("id_edited")
        date = request.POST.get("date_edited")
        desc = request.POST.get("desc_edited")
        amount = request.POST.get("amount_edited")
        
        # edit info and save in the expenses table
        
        filt_exp = Expenses.objects.get(exp_id = id)
        filt_exp.exp_date = date
        filt_exp.exp_desc = desc
        filt_exp.exp_amount = amount 
        filt_exp.exp_creator = request.user
        filt_exp.save()
        
        data = {}
        
        return JsonResponse(data,status=200)
        
        
    


    
