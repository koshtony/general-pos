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
from .models import Stocks,Shops,Sales,Expenses,Location,Tasks
from datetime import datetime
import json
import time
import os
# Create your views here.

orders = [
    {
        'title':"today orders",
        'qty':10
    },
    
]
def home(request):
    tasks = Tasks.objects.all()
    data={
        "orders":orders,
        "tasks":tasks
    }
    return render(request,'firstapp/home.html',data)

#==============render counter page =================

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

# =============renders visuals page =================
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

#============= gets info of the selected item===========
#============= item added to cart=======================

def getCounter(request):
    pids = request.GET.get("pid")
    
    qty = request.GET.get("qty")
    
    product = Stocks.objects.get(p_id=pids)
    
    name  = product.p_name
    serial = product.p_serial
    cat =product.p_category
    shops = product.p_shop.shop_id
    price = product.p_price
    cost = product.p_cost
    total = float(price)*int(qty)
    total_cost = float(cost)*int(qty) 
    profit = total-total_cost
    
    
    pid = hash(time.time())+int(pids)
    
    data ={pid:
        
            {
                "key":pid,"serial":serial,"name":name,"category":cat,"shops":shops,
                "qty":qty,"price1":price,"price":total,"cost1":cost, "cost":total_cost,
                "profit":profit
                
            }
                
        }
    
    

    if request.session.has_key('sales'):
        if pid not in request.session["sales"]:
            request.session["sales"] = dict(list(request.session["sales"].items())+ list(data.items()))
       
    else:
        request.session["sales"] = data
            
    
  
   
    filt_data = Stocks.objects.filter(p_name=name).first()
    new_obj=Stocks.objects.get(p_name=name)
    new_obj.p_qty = filt_data.p_qty - int(qty)
    new_obj.save()
    return JsonResponse(data,status=200)

def counterPlusSess(request):
    key = request.GET.get("key")
    qty = request.GET.get("qty")
   
   
    if 'sales' in request.session:
        request.session["sales"][key]["qty"]=qty
        
        request.session["sales"][key]["price"] = float(request.session["sales"][key]["price1"])*float(qty)
       
        request.session["sales"][key]["profit"] = float(request.session["sales"][key]["price1"])*float(qty) -  request.session["sales"][key]["cost1"]*float(qty)
        
        request.session["sales"] = request.session["sales"]
    key = {"key":key}
    
    return JsonResponse(key)

def counterMinusSess(request):
    key = request.GET.get("key")
    qty = request.GET.get("qty")
    
    if 'sales' in request.session:
        request.session["sales"][key]["qty"]=qty
        
        request.session["sales"][key]["price"] = float(request.session["sales"][key]["price1"])*float(qty)
        
        request.session["sales"][key]["profit"] = float(request.session["sales"][key]["price1"])*float(qty) -  request.session["sales"][key]["cost1"]*float(qty)
        
        request.session["sales"] = request.session["sales"]
    key = {"key":key}
    return JsonResponse(key)

def counterRemvSess(request):
    key = request.GET.get('key')
    
    if 'sales' in request.session:
        print(request.session["sales"][key])
        del request.session["sales"][key]
        request.session["sales"] = request.session["sales"]
        
    data ={"key":key}
    
    return JsonResponse(data)

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

# ======view to handle filter post query ==============

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

#=====view to handle stocks addittion=====
    
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

#========handles stocks updates ===========


class StocksUpdateView(UpdateView):
    model = Stocks
    
    template_name = 'firstapp/update_stocks.html'
    
    fields = ['p_name','p_category','p_desc',
              'p_image','p_qty','p_price','p_cost','p_created'
              ]
    
    def form_valid(self,form):
        form.instance.p_creator = self.request.user
        return super().form_valid(form)


#========add stocks simple method ========

def StocksInbound(request):
    if request.POST:

        item = request.POST.get("item")
        shop = request.POST.get("shop")
        qty = request.POST.get("qty")
        remarks = request.POST.get("remarks")
        
        # filter stocks by product name and edit 

        filt_stocks = Stocks.objects.filter(p_name = item).first()
        filt_stocks.p_shop.shop_name = shop
        filt_stocks.p_qty = filt_stocks.p_qty + int(qty)
        filt_stocks.p_creator = request.user 
        filt_stocks.p_created = datetime.now()
        filt_stocks.save()

        data = {"remarks":remarks}
    
        
        return JsonResponse(data,status=200)

#==========Transfer bulky quantity ===========

def StocksTransfer(request):
    if request.POST:
        from_ = request.POST.get("shop1")
        to_ = request.POST.get("shop2")
        qty = request.POST.get("qty")
        item = request.POST.get("item")
        
        filt_shop_1 = Shops.objects.filter(shop_name=from_).first()
        filt_stocks_1 = Stocks.objects.filter(p_name = item).filter(p_shop = filt_shop_1.shop_id).first()
        print(filt_stocks_1)
        filt_shop_2 = Shops.objects.filter(shop_name = to_).first()
        filt_stocks_2 = Stocks.objects.filter(p_name = item).filter(p_shop = filt_shop_2.shop_id).first()
        print(filt_stocks_2)
        
        try:
            
            filt_stocks_1.p_qty = filt_stocks_1.p_qty - int(qty)
            filt_stocks_2.p_qty = filt_stocks_1.p_qty + int(qty)
            filt_stocks_2.save()
            
            
 
            data = {"success":"success"}
            
        except:
            mssg = ''
            if filt_stocks_2 == None:
            #filt_stocks_1.p_qty = filt_stocks_1.p_qty - int(qty)
                stock_ = Stocks(
                    
                    p_serial = filt_stocks_1.p_serial,
                    p_name = item,
                    p_category = filt_stocks_1.p_category,
                    p_desc = filt_stocks_1.p_desc,
                    p_image = filt_stocks_1.p_image,
                    p_qty = qty,
                    p_price = filt_stocks_1.p_price,
                    p_cost = filt_stocks_1.p_cost,
                    p_shop = filt_shop_2,
                    p_creator = request.user,
                    p_created = datetime.now()
                    
                )
                filt_stocks_1.save()
                stock_.save()
                mssg += "matching error but item transferred, duplicate created "
                
             
            else:
                mssg +="error"
            
            data = {"error":mssg}



                       
        

        return JsonResponse(data,status=200)
    
#=======display the shops details========

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

#==========update shop post request==

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
    dir= os.path.dirname(os.path.abspath(__file__))
    if data != None:
        data = '<html>'+data + '</html>'
        html_path =  dir+"/static/firstapp/exports/invoice.html"
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
        
        
    
#=============handles (location) coordinates storage and audit==

def HandleLoc(request):

    if request.POST:
        lat = request.POST.get("lat")
        long_ = request.POST.get("long")

        location = Location(

                    latitude = lat,
                    longitude = long_,
                    loc_tag = "normal",
                    loc_created = datetime.now(),
                    loc_creator = request.user
            )
        location.save()

        data = {"latitude":lat,"longitude":long_}

        return JsonResponse(data,status=200)

#===========displays location/attendance info

def ShowLoc(request):

    location = Location.objects.all()

    contxt = {
                   "locs":location
                }
    
    return render(request,"firstapp/location.html",contxt)


def ShowTasks(request):

    tasks = Tasks.objects.all()

    contxt = { 
                  "tasks":tasks

                }

    return render(request,"firstapp/tasks.html",contxt)