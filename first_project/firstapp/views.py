from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import ListView,CreateView,UpdateView,DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.templatetags.static import static
from django.utils.decorators import method_decorator
from .models import Stocks,Shops,Sales
from datetime import datetime
import pdfkit
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
    data ={pid:
        
            {
                "serial":serial,"name":name,"category":cat,"shops":shops,
                "qty":qty,"price":total,"cost":total_cost,
                "profit":profit
                
            }
                
        }
    
    pass_data = {"name":name,"qty":qty,"price":price,"total":total}

    if request.session.has_key('sales'):
        
            request.session["sales"] = dict(list(request.session["sales"].items())+ list(data.items()))
    
    else:
        request.session["sales"] = data
            
        
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
    if request.POST:
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        if date1!='' or date1!='':
            products = Stocks.objects.filter(p_created__gte=date1,p_created__lte=date2)
        else: 
            products = Stocks.objects.all()
        
        page_num = request.GET.get('page',1)
        paginator = Paginator(products,5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger: 
            page_obj =paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
            
        contxt = {
            'products':products,
            'page_obj': page_obj
        }
        
        return render(request,'firstapp/stocks.html',contxt)
    return render(request,'firstapp/stocks.html')

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
    paginate_by = 5
    
    def get_queryset(self):
        if self.request.GET:
            date1 = self.request.GET.get("date1")
            date2 = self.request.GET.get("date2")
            queryset =  Sales.objects.filter(s_created__gte=date1,s_created__lte=date2)
        
            return queryset
        return super().get_queryset()
    
def OrdersView(request):
    return render(request, 'firstapp/orders_list.html')

def InvoiceView(request):
    data = request.GET.get("htmlData")
    if data != None:
        data = '<html>'+data + '</html>'
        html_path =  "/home/koshtech/Videos/general-pos/first_project/firstapp/static/firstapp/exports/invoice.html"
        pdf_path = "/home/koshtech/Videos/general-pos/first_project/firstapp/static/firstapp/exports/invoice.pdf"
        with open(html_path,"w+") as file:
        
            file.write(data)
            
        pdfkit.from_file(html_path,pdf_path)
        
    return render(request,'firstapp/invoice.html',{'filename':'invoice.pdf'})