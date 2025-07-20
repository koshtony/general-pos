from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.db.models import Sum,IntegerField
from django.db.models.functions import Cast
from django.db.models.functions import TruncDate
from django.views.generic import ListView,CreateView,UpdateView,DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.templatetags.static import static
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
from .models import Stocks,Shops,Sales,Expenses,Location,\
Tasks,Debts,Paid,Contacts,mpesaPay,Cart
from posUsers.models import Profile
from .sms import send_text
from .mpesa import stk_push,c_2_b_reg_url,sim_c_2_b,get_token
from .summary import sales_summ,stocks_summ,time_sales_summ,sales_summary,exp_summary,today_summary,monthly_comp
from .data_transfer import connect_sql
from datetime import datetime,timedelta,date
import requests
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

@login_required
def home(request):
    
    profit = Sales.objects.aggregate(Sum("s_profit"))["s_profit__sum"]
    expenses = Expenses.objects.aggregate(Sum("exp_amount"))["exp_amount__sum"]
    revenue = Sales.objects.aggregate(Sum("s_price"))["s_price__sum"]
    sales_qty = Sales.objects.aggregate(Sum("s_qty"))["s_qty__sum"]
    profit = profit - expenses
    shops = Shops.objects.all()
    users = User.objects.all()
    
    profit_per_store = Sales.objects.values('s_shop').annotate(total_profit=Sum('s_profit'))
    revenue_per_store = Sales.objects.values('s_shop').annotate(total_revenue=Sum('s_price'))
    expenses_per_store = Expenses.objects.values('exp_shop').annotate(total_expenses=Sum('exp_amount'))
    sales_per_store = Sales.objects.values('s_shop').annotate(total_sales=Sum('s_qty'))
    sales_per_store_per_product = Sales.objects.values('s_name').annotate(total_sales=Sum('s_qty'))
    sales = Sales.objects.all()
    
  
    
    sales_per_store_per_product = Sales.objects.values('s_name').annotate(total_sales=Sum('s_qty'))
    
    print(expenses_per_store)
    data = {
        "profit":f"Ksh {profit}" if profit is not None else profit,
        "expenses":f"Ksh {expenses}" if expenses is not None else expenses,
        "revenue":f"Ksh {revenue}" if revenue is not None else revenue,
        "sales_qty":f"{sales_qty}" if sales_qty is not None else sales_qty,
        "profit_per_store":profit_per_store, 
        "revenue_per_store":revenue_per_store,
        "expenses_per_store":expenses_per_store,
        "sales_per_store":sales_per_store,
        "sales":sales,
        "shops":shops,
        "users":users,
       
        "sales_per_store_per_product":sales_per_store_per_product
    }
    
    return render(request,'firstapp/home.html',data)

#=============dashboard filter================
def home_filter(request):
    
    if request.method == "POST":
        from_date = request.POST.get("dateFrom")
        to_date = request.POST.get("dateTo")
        shop_id = request.POST.get("shops")
        #user_id = request.POST.get("user")
        
        
       
        try:
            start_date = datetime.strptime(from_date, "%Y-%m-%d")
            end_date = datetime.strptime(to_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid date format"}, status=400)

        # Optional filtering conditions
        sales_filtered = Sales.objects.filter(s_created__range=(start_date, end_date))
        expenses_filtered = Expenses.objects.filter(exp_date__range=(start_date, end_date))

        if shop_id:
            
            shop_name = Shops.objects.get(shop_id=shop_id).shop_name
            sales_filtered = sales_filtered.filter(s_shop__shop_id=int(shop_id))
            print(sales_filtered)
            expenses_filtered = expenses_filtered.filter(exp_shop=shop_name)

      

        # Aggregates
        profit = sales_filtered.aggregate(Sum("s_profit"))["s_profit__sum"] or 0
        expenses = expenses_filtered.aggregate(Sum("exp_amount"))["exp_amount__sum"] or 0
        print(expenses)
        revenue = sales_filtered.aggregate(Sum("s_price"))["s_price__sum"] or 0
        sales_qty = sales_filtered.aggregate(Sum("s_qty"))["s_qty__sum"] or 0
        net_profit = profit - expenses

        # Per-store/grouped aggregates
        profit_per_store = sales_filtered.values('s_shop').annotate(total_profit=Sum('s_profit'))
        revenue_per_store = sales_filtered.values('s_shop').annotate(total_revenue=Sum('s_price'))
        expenses_per_store = (
            expenses_filtered
            .values('exp_shop')
            .annotate(total_expenses=Sum('exp_amount'))
        )
        sales_per_store = sales_filtered.values('s_shop').annotate(total_sales=Sum('s_qty'))
        sales_per_product = sales_filtered.values('s_name').annotate(total_sales=Sum('s_qty'))
        shops = Shops.objects.all()
        
        print(expenses_per_store)

        # Render HTML or return JSON/partial
        data = {
            "profit": net_profit,
            "revenue": revenue,
            "expenses": expenses,
            "sales_qty": sales_qty,
            "profit_per_store": profit_per_store,
            "revenue_per_store": revenue_per_store,
            "expenses_per_store": expenses_per_store,
            "sales_per_store": sales_per_store,
            "sales_per_product": sales_per_product,
            "shops":shops,
        }

        return render(request, "firstapp/home_filter.html", data) 
        
    
    return JsonResponse({"error": "Invalid request"}, status=400)


#===========simple counter =============
@login_required
def simple_counter(request):
    
    shops = Shops.objects.filter(shop_auth__username = request.user.username)
    
    
    
    shops_ids = [shop.shop_id for shop in shops]
    
    stocks = cache.get('stocks')
    
    if stocks is None:
        
        stocks = Stocks.objects.filter(p_shop__shop_id__in = shops_ids).order_by('-p_created')
        cache.set("stocks",stocks)
    
    carts = Cart.objects.all().order_by('-pk')
    
    
    sub_total = sum([0 if cart.cart_stock == None else (cart.cart_stock.p_price * cart.qty) for cart in carts])
    vat = sum([0 if cart.cart_stock==None else cart.cart_stock.p_vat*(cart.cart_stock.p_price * cart.qty) for cart in carts])
    
    total = sub_total + vat
    
    contxt = {"stocks":stocks,"carts":carts,"total":total,"vat":vat,"sub_total":sub_total}
    
    return render(request,'firstapp/simple_counter.html',contxt)

@login_required 
def add_to_cart(request,id):
    
    stock = Stocks.objects.get(pk=id)
    
    cart = Cart(
        cart_stock = stock ,
        price = stock.p_price,
        order_code = "ORD"+str(datetime.now().strftime('%Y%m%d%H%M%S%f'))
    )
    
    cart.save()
    
    carts = Cart.objects.all().order_by('-pk')
    
    sub_total = sum([cart.price for cart in carts])
    vat = sum([cart.cart_stock.p_vat*cart.price for cart in carts])
    
    total = sub_total + vat
     
    
    contxt = {"carts":carts,"total":total,"vat":vat,"sub_total":sub_total}
    
    
    
    return render(request,'firstapp/cart.html',contxt)
@csrf_exempt
def update_cart_qty(request,id):
    
    new_qty = float(request.POST.get("itemQty"))
    
    
    
    cart = Cart.objects.get(pk=id)
    cart.qty = new_qty
    cart.price = new_qty * cart.cart_stock.p_price
    cart.save()
    
    carts = Cart.objects.all().order_by('-pk')
    
    sub_total = sum([cart.price for cart in carts])
    vat = sum([cart.cart_stock.p_vat*cart.price for cart in carts])
    
    total = sub_total + vat
     
    
    contxt = {"carts":carts,"total":total,"vat":vat,"sub_total":sub_total}
    
    return render(request,'firstapp/cart.html',contxt)

def del_cart_item(request,id):
    
    cart = Cart.objects.get(pk=id)
    cart.delete()
    
    carts = Cart.objects.all().order_by('-pk')
    
    sub_total = sum([cart.price for cart in carts])
    vat = sum([cart.cart_stock.p_vat*cart.price for cart in carts])
    
    total = sub_total + vat
     
    
    contxt = {"carts":carts,"total":total,"vat":vat,"sub_total":sub_total}
    
    return render(request,'firstapp/cart.html',contxt)

# search items by scanning 
@csrf_exempt
def search_by_scan(request):
    
    serial = request.POST.get("serial")
    stocks = Stocks.objects.filter(p_serial = serial)
    
    contxt = {"stocks":stocks}
    
    return render(request,'firstapp/filter_stocks.html',contxt)
    

@csrf_exempt
def search_by_name(request):
    
    name = request.POST.get("name")
    stocks = Stocks.objects.filter(p_name__contains = name)
    
    contxt = {"stocks":stocks}
    
    return render(request,'firstapp/filter_stocks.html',contxt)
    
@csrf_exempt
def search_by_category(request):
    
    category = request.POST.get("category")
    stocks = Stocks.objects.filter(p_category__contains = category)
    
    contxt = {"stocks":stocks}
    
    return render(request,'firstapp/filter_stocks.html',contxt)

@csrf_exempt
def search_by_desc(request):
    
    desc = request.POST.get("desc")
    stocks = Stocks.objects.filter(p_desc__contains = desc)
    
    contxt = {"stocks":stocks}
    
    return render(request,'firstapp/filter_stocks.html',contxt)

def print_cart_receipt(request):
    
    carts = Cart.objects.all().order_by('-pk')
    
    sub_total = round(sum([cart.price for cart in carts]),2)
    vat = sum([cart.cart_stock.p_vat*cart.price for cart in carts])
    
    total = round(sub_total + vat,2)
     
    shop_name = carts[0].cart_stock.p_shop.shop_name
    shop_cat = carts[0].cart_stock.p_shop.shop_cat
    shop_loc = carts[0].cart_stock.p_shop.shop_loc
    shop_terms = carts[0].cart_stock.p_shop.shop_terms
    contxt = {
        "carts":carts,"total":total,"vat":vat,"sub_total":sub_total,
        "shop_name":shop_name,"shop_loc":shop_loc,"shop_cat":shop_cat,
        "shop_terms":shop_terms,
        "date":datetime.now(),
        "order_code":carts[0].order_code,
        "user_names":f'{request.user.profile.first} {request.user.profile.surname}'
        
        }
    
    
    
    return render(request,'firstapp/simple_receipt.html',contxt)

def cart_to_sales(request):
    
    carts = Cart.objects.all()
    msg = ''
    if len(carts)>0:
       
            
        try:
            for cart in carts:
                sale = Sales(
                    s_serial = cart.cart_stock.p_serial,
                    s_name = cart.cart_stock.p_name,
                    s_shop = cart.cart_stock.p_shop,
                    s_qty = cart.qty,
                    s_price = cart.price,
                    s_cost = cart.cart_stock.p_cost * cart.qty,
                    s_negatives = 0,
                    s_profit = cart.price - cart.cart_stock.p_cost * cart.qty,
                    s_type = "cash",
                    s_status = "sold",
                    s_order_code = cart.order_code,
                    s_creator = request.user
                    
                    
                    
                )
                sale.save()
                stock = cart.cart_stock
                stock.p_qty = stock.p_qty-cart.qty
                stock.save()
                cart.delete()
                
            msg += '<strong style="color:green">SUCCESS: Sale saved successfully </strong>'
                
        except Exception as err:
                
                msg += f'<strong style="color:red">SERVER ERR: {err}</strong>'
        
                
                
            
        pass
    else:
        msg+='<strong style="color:green">FAILED: cart is empty</strong>'
    
    return HttpResponse(msg)

def clear_cart(request):
    msg = ''
    try:
        Cart.objects.all().delete()
        
        msg+='<strong style="color:orange">SUCCESS: cart deleted successfully</strong>'
        
    except Exception as err:
        
        msg += f'<strong style="color:green">FAILED: {err}</strong>'
        
    carts = Cart.objects.all().order_by('-pk')
    
    sub_total = sum([cart.price for cart in carts])
    vat = sum([cart.cart_stock.p_vat*cart.price for cart in carts])
    
    total = sub_total + vat
     
    
    contxt = {"carts":carts,"total":total,"vat":vat,"sub_total":sub_total}
    
    return render(request,'firstapp/cart.html',contxt)
    
    
    
def transfer_data(request):
    
    df = connect_sql()
    
    for idx in df.index:
        
        stock = Stocks(
            p_name = df["name"][idx],
            p_category = df["category"][idx],
            p_desc = df["desc"][idx],
            p_qty = df["qty"][idx],
            p_price = df["price"][idx],
            p_cost = df["cost"][idx],
            p_vat = 0.16,
            p_shop = Shops.objects.get(shop_name = 'Touch & Light'),
            p_creator = request.user,
        
            
            
        )
        stock.save()
    
    return HttpResponse("done")  
        
        
        
        
        
        
        
#==============render counter page =================
@login_required
def counter(request):
    
    sums = 0
    
    if 'sales' in request.session:
        for key,value in request.session["sales"].items():
            sums+=float(request.session["sales"][key]["price"])
            
  
    stocks = {
        'products': Stocks.objects.all(),"users":Profile.objects.all(),
        'sum':sums
        
    }
    return render(request,'firstapp/counter.html',stocks)

#===========render cashier page ======================
@login_required
def cashier(request):
    
    contxt = {
        "users":Profile.objects.all(),
        "sales":Sales.objects.all()
      
    }
    return render(request,'firstapp/cashier.html',contxt)



# =============renders visuals page =================
@login_required
def Charts(request):
    sales = Sales.objects.values('s_name').annotate(total=Sum('s_price'))
    expenses = Expenses.objects.values('exp_shop').annotate(total=Sum('exp_amount'))
    stocks = Stocks.objects.values('p_name').annotate(total=Sum('p_qty'))
    sales_by_date = (
        Sales.objects.annotate(date=TruncDate("s_created"))
        .values("date")
        .annotate(total=Sum("s_price"))
        .order_by("date")
    )
    
    profit_by_date = (
    Sales.objects.annotate(date=TruncDate("s_created"))
    .values("date")
    .annotate(total=Sum("s_profit"))
    .order_by("date")
)

    # Time series expenses per day
    expenses_by_date = (
        Expenses.objects.annotate(date=TruncDate("exp_date"))
        .values("date")
        .annotate(total=Sum("exp_amount"))
        .order_by("date")
    )

    # Time series stock changes per day (assuming you store changes)
    stocks_by_date = (
        Stocks.objects.annotate(date=TruncDate("p_created"))
        .values("date")
        .annotate(total=Sum("p_qty"))
        .order_by("date")
    )
    
    sales_by_date = [
    {"date": entry["date"].strftime("%Y-%m-%d"), "total": entry["total"]}
    for entry in sales_by_date
    ]
    
    profit_by_date = [
    {"date": entry["date"].strftime("%Y-%m-%d"), "total": float(entry["total"] or 0)}
    for entry in profit_by_date
    ]

    expenses_by_date = [
        {"date": entry["date"].strftime("%Y-%m-%d"), "total": entry["total"]}
        for entry in expenses_by_date
    ]

    stocks_by_date = [
        {"date": entry["date"].strftime("%Y-%m-%d"), "total": entry["total"]}
        for entry in stocks_by_date
    ]
    
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1)

    sales_data = Sales.objects.filter(s_created__gte=start_of_month).values('s_name').annotate(
        sales=Sum('s_qty'),
        revenue=Sum('s_price'),
        profit=Sum('s_profit')
    )

    chart_data = [
        {
            "product": row["s_name"],
            "sales": row["sales"] or 0,
            "revenue": row["revenue"] or 0,
            "profit": row["profit"] or 0
        }
        for row in sales_data
    ]

        
    context = {
            "sales": sales,
            "expenses": expenses,
            "stocks": stocks,
            "sales_by_date": sales_by_date,
            "profit_by_date": profit_by_date,
            "expenses_by_date": expenses_by_date,
            "stocks_by_date": stocks_by_date,
            "sales_profit_revenue_data": chart_data,
    }
    return render(request, "firstapp/reports.html", context)

#============= gets info of the selected item===========
#============= item added to cart=======================
@login_required
def scanCounter(request):

    if request.POST:
        barcode = request.POST.get("barcode")
        print(barcode)
        
        try:
            product = Stocks.objects.filter(p_serial=barcode)[0]
            pid = str(hash(time.time())+int(product.p_id))
            data = {pid:{
                "key":pid,"serial":barcode,"name":product.p_name,
                "category":product.p_category,"shops":product.p_shop.shop_id,"qty":1,
                "price1":product.p_price,"price":product.p_price,"cost1":product.p_cost,
                "cost":product.p_cost,"profit":product.p_price-product.p_cost,"disc":0,
                "waiter":request.user.username
            }

            }

            if request.session.has_key('sales'):
                request.session["sales"] = dict(list(request.session["sales"].items())+ list(data.items()))

            else:

                request.session["sales"] = data

            scanned_stock = Stocks.objects.filter(p_serial=barcode).first()
            rem_stock = Stocks.objects.filter(p_serial=barcode).first()
            rem_stock.p_qty = scanned_stock.p_qty-1 
            rem_stock.save()
            return JsonResponse(data,status=200)
        except Exception as e:
            
            data = "error!! serial no -> not found"
            print(data)
            return JsonResponse(data,safe=False)
        

@login_required
def getCounter(request):

    if request.POST:
        keys = request.POST.get("keys")
        pids = request.POST.get("pid")
        qty = request.POST.get("qty")
        disc = request.POST.get("disc")
        waiter = request.POST.get("waiter")

        product = Stocks.objects.get(p_id=pids)
        
        name  = product.p_name
        serial = product.p_serial
        cat =product.p_category
        shops = product.p_shop.shop_id
        price = product.p_price
        cost = product.p_cost
        total = (float(price)*int(qty))-float(disc)
        total_cost = float(cost)*int(qty) 
        profit = total-total_cost
        
        if keys == '':
        
            pid = str(hash(time.time())+int(pids))
            data ={pid:
                    
                        {
                            "key":pid,"serial":serial,"name":name,"category":cat,"shops":shops,
                            "qty":qty,"price1":price,"price":total,"cost1":cost, "cost":total_cost,
                            "profit":profit,"disc":disc,"waiter":waiter
                            
                        }
                            
                    }

        elif keys != '':  
            pid = str(hash(time.time())+int(pids))
            data ={pid:
                    
                        {
                            "key":keys,"serial":serial,"name":name,"category":cat,"shops":shops,
                            "qty":qty,"price1":price,"price":total,"cost1":cost, "cost":total_cost,
                            "profit":profit,"disc":disc,"waiter":waiter
                            
                        }
                            
                    }
        
        

        if request.session.has_key('sales'):
                request.session["sales"] = dict(list(request.session["sales"].items())+ list(data.items()))
           

           
        else:
            request.session["sales"] = data
                
        
      
       
        filt_data = Stocks.objects.filter(p_name=name).first()
        new_obj=Stocks.objects.filter(p_name=name).first()
        new_obj.p_qty = filt_data.p_qty - int(qty)
        new_obj.save()
        return JsonResponse(data,status=200)
@login_required
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
@login_required
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

@login_required
def counterRemvSess(request):
    key = request.GET.get('key')
    
    if 'sales' in request.session:
        print(request.session["sales"][key])
        del request.session["sales"][key]
        request.session["sales"] = request.session["sales"]
        
    data ={"key":key}
    
    return JsonResponse(data)
# ==== add unpaid sales =====
@login_required
def addSales(request):
    if request.POST:
        code = request.POST.get("code")
        waiter = request.POST.get("waiter")
        print(len(code))
        if 'sales' in request.session and len(code)>0:
            keys_to_del = []
            for key,value in request.session["sales"].items():
                    #if request.session["sales"][key]["key"] == code:

                        sales= Sales(
                            s_serial = code,
                            s_name = request.session["sales"][key]["name"],
                            s_shop = Shops.objects.get(shop_id=request.session["sales"][key]["shops"] ),
                            s_qty = request.session["sales"][key]["qty"],
                            s_price = request.session["sales"][key]["price"],
                            s_cost = request.session["sales"][key]["cost"],
                            s_negatives = 0,
                            s_profit = request.session["sales"][key]["profit"],
                            s_created = datetime.now(),
                            s_creator = User.objects.get(username=waiter)
                        )
                        sales.save()

                        keys_to_del.append(key)
        
            for i in keys_to_del:
                del request.session["sales"][i]
            request.session["sales"] = request.session["sales"]

            return JsonResponse("Transaction for recipt no: "+code+" complete",safe=False)
    
        return JsonResponse("no sale to submit",safe=False)   
    
@login_required
def addPaid(request):
    
    if request.POST:
        receipt = request.POST.get("receipt")
        waiter = request.POST.get("waiter")
    
        msg = ''
        try:
            if receipt != '':
                sales = Sales.objects.filter(s_serial=str(receipt)).all()
                print(receipt)
                receipts = []
                for sale in sales:
                    print(sale)
                    paid = Paid(
                    
                        sn = sale.s_serial,
                        product = sale.s_name,
                        qty = sale.s_qty,
                        amount = sale.s_price,
                        profit = sale.s_profit,
                        pay_type = "paid",
                        waiter = User.objects.get(username=waiter),
                        date = datetime.now()
                            
                        
                    )
                    receipts.append(sale.s_serial)
                    paid.save()
                    sale.delete()
                msg += receipts[0]+" paid successfully"
            else:
                
                msg += "no receipt to transact"
        except Exception as e:
            print(e)
            msg += "failed ensure receipt is correct"
        return JsonResponse(msg,safe=False)
            
@login_required
def addContact(request):
    
    if request.POST:
        
        name = request.POST.get("name") 
        phone = request.POST.get("phone")  
        
        contact = Contacts(cont_name = name, cont_phone = phone, cont_created = datetime.now())
        
        contact.save()
        
        return JsonResponse("contact added successfully",safe=False)
'''
     send text message to all saved contacts
'''
    
@login_required
def sendSms(request):
    
    if request.POST:
        
        sms = request.POST.get("sms")
        
        resp = []
        
      
        for contact in Contacts.objects.all():
            
            res = send_text(contact.cont_phone,sms)
            
            resp.append(res)
            
        
        return JsonResponse(resp,safe=False)
        
        
    
@login_required
def getContact(request):
    
    contacts = Contacts.objects.all()
    
    contacts = serializers.serialize('json',contacts)
    
    return JsonResponse(contacts,safe=False)
    
    
    
@login_required
def stocksView(request): 
    
    shops = Shops.objects.filter(shop_auth__username = request.user.username)
    
    shops_ids = [shop.shop_id for shop in shops]
    
    products = cache.get('stocks')
    
    
    
    if products is None:
        
        if request.user.is_superuser or request.user.is_staff:
        
            products = Stocks.objects.all().order_by('-p_created')
            cache.set('stocks',products)
            
        else: 
            
            products = Stocks.objects.filter(p_shop__shop_id__in = shops_ids).order_by('-p_created')
           
            cache.set('stocks',products)
            
            
        
    
            
    contxt = {
            'products':products,
    }
    return render(request,'firstapp/stocks.html',contxt)

# ======view to handle filter post query ==============
@login_required
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
    
@login_required
def filter_stocks_by_date(request):
    
    if request.POST:
        
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        
        if date1!='' or date1!='':
            products = Stocks.objects.filter(p_created__gte=date1,p_created__lte=date2)
            
        else: 
            
            products = Stocks.objects.all()
            
    contxt = {"products":products}
            
    return render(request,"firstapp/filter_stocks.html",contxt)

#=====view to handle stocks addittion=====
    
class StocksCreateView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    model = Stocks
    
    template_name = 'firstapp/add_stocks.html'
    
    fields = ['p_name','p_serial','p_category','p_desc',
              'p_image','p_qty','p_price','p_cost','p_vat','p_disc','p_shop','p_creator','p_created'
              ]
    
    success_message = "item added successfully"
    
    success_url = reverse_lazy('firstapp-addstocks')
    
    def form_valid(self,form):
        form.instance.p_creator = self.request.user
        return super().form_valid(form)
    
class StocksDetailView(DetailView):
    model= Stocks

#========handles stocks updates ===========


class StocksUpdateView(LoginRequiredMixin,UpdateView):
    model = Stocks
    
    template_name = 'firstapp/update_stocks.html'
    
    fields = ['p_name','p_serial','p_category','p_desc',
              'p_image','p_qty','p_price','p_cost','p_vat','p_disc','p_shop','p_creator','p_created'
              ]
    
    def form_valid(self,form):
        form.instance.p_creator = self.request.user
        return super().form_valid(form)
    



#========add stocks simple method ========
@login_required
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
@login_required
def StocksTransfer(request):
    if request.POST:
        from_ = request.POST.get("shop1")
        to_ = request.POST.get("shop2")
        qty = request.POST.get("qty")
        item = request.POST.get("item")
        
        filt_shop_1 = Shops.objects.filter(shop_name=from_).first()
        filt_stocks_1 = Stocks.objects.filter(p_name = item).filter(p_shop = filt_shop_1.shop_id).first()
        
        filt_shop_2 = Shops.objects.filter(shop_name = to_).first()
        filt_stocks_2 = Stocks.objects.filter(p_name = item).filter(p_shop = filt_shop_2.shop_id).first()
      
        
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
    
#====low stocks notifications============
def low_stocks_alert(request): 
    
    low_stock_items = Stocks.objects.filter(p_qty__lte=5)
    data = list(low_stock_items.values("p_name", "p_qty"))
    return JsonResponse({"low_stock": data})
    
    
    
#=======display the shops details========

class ShopsListView(LoginRequiredMixin,ListView):
    model =Shops
    template_name = 'firstapp/shops_list.html'
    context_object_name = 'shops'
    paginate_by = 5
    

class ShopsCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Shops
    
    template_name = 'firstapp/add_shops.html'
    
    success_message = ' shop added successfully'
    
    fields =['shop_name','shop_cat','shop_loc','shop_terms','shop_auth']
    
    def form_valid(self,form):
        return super().form_valid(form)

#==========update shop post request==

@login_required
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

def SalesListView(request):
    shops = Shops.objects.filter(shop_auth__username = request.user.username)
    
    shops_ids = [shop.shop_id for shop in shops]
            
    sales =  Sales.objects.filter(s_shop__shop_id__in=shops_ids).order_by('-s_created')
    
    contxt = { 
                "sales":sales
              
              }
    
    
    return render(request,'firstapp/sales_list.html',contxt)
    
    

@login_required    
def salesPostView(request):
    if request.POST:
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        if date1!='' or date1!='':
            sales = Sales.objects.filter(s_created__gte=date1).filter(s_created__lte=date2)
            sales = serializers.serialize('json',sales)
           
            
        else: 
            sales = Sales.objects.all().values()
            sales = serializers.serialize('json',sales)
        
        return JsonResponse(sales,safe=False)
    
    
@login_required
def filter_sales_by_date(request):
    
    if request.POST:
        
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        
        if date1!='' or date1!='':
            sales = Sales.objects.filter(s_created__gte=date1).filter(s_created__lte=date2)
            
        else: 
            
            sales = Sales.objects.all() 
            
    contxt = {"sales":sales}
            
    return render(request,"firstapp/filter_sales.html",contxt)
            
            
    
            
            
    
            
             
        
        
        

#==========handles return of items======//moves from sales table to stocks table

@login_required
def SalesReturn(request):
    if request.method:
        
        id = int(request.POST.get("id"))
        name = request.POST.get("name")
        qty = float(request.POST.get("qty"))
        
        # filter both sales and stocks by id and name resp...
        sales_filt = Sales.objects.get(s_id = id)
        stocks_filt = Stocks.objects.filter(p_name = sales_filt.s_name).first()
        
        # removes from sales -qty and adds to stocks +qty
        try:
            # deducting from sales
            
            sales_filt.s_qty = sales_filt.s_qty-qty
            sales_filt.s_cost = sales_filt.s_qty*stocks_filt.p_cost
            sales_filt.s_price = sales_filt.s_qty*stocks_filt.p_price
            sales_filt.s_profit = (sales_filt.s_qty*stocks_filt.p_price)-(sales_filt.s_qty*stocks_filt.p_cost)
            sales_filt.s_creator = request.user
            sales_filt.s_status = "returned"
            sales_filt.s_created = datetime.now()
            
            sales_filt.save()
            
            # adding to stocks
            
            stocks_filt.p_qty = stocks_filt.p_qty + qty
            stocks_filt.p_creator = request.user
            stocks_filt.p_created = datetime.now()
            stocks_filt.save()
            
            mssg = {"success":"item returned successfully"}
            
        except Exception as e:
             
             mssg = {"error":"failed to return"}
        print(mssg) 
        return JsonResponse(mssg,status=200)
            
@login_required        
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

@login_required
def financeView(request):
    
    
    
    contxt = {
                  "expenses":Expenses.objects.all(),
                  "sum": Expenses.objects.aggregate(Sum("exp_amount"))["exp_amount__sum"] +  Debts.objects.aggregate(Sum('debt_rem'))["debt_rem__sum"],
                  "profit": Sales.objects.aggregate(Sum("s_profit"))["s_profit__sum"]-Debts.objects.aggregate(Sum('debt_rem'))["debt_rem__sum"],
                  "net_profit": Sales.objects.aggregate(Sum("s_profit"))["s_profit__sum"]-Expenses.objects.aggregate(Sum("exp_amount"))["exp_amount__sum"],
                  "shops": Shops.objects.all(),
              
              }
    return render(request,'firstapp/financials.html',contxt)
@login_required
def financePostView(request):
   
    if request.POST:
        date = request.POST.get("date")
        desc = request.POST.get("desc")
        amount = request.POST.get("amount")
        shop = request.POST.get("shop")
    
        exp = Expenses(exp_desc = desc,exp_amount = amount , 
                       exp_date = date, exp_shop=shop,exp_creator=request.user
                       )
        exp.save()
        
        return JsonResponse({'msg':"added successfully"})
    
#==========handles post requests from expenses page ======
@login_required
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
        
@login_required
def financeSummary(request):
    
    contxt = {
        
        "summary": json.dumps(sales_summary(Sales)+exp_summary(Expenses),default=str)
    }
    print(contxt)
    print(exp_summary(Expenses))
    return render(request,'firstapp/summary.html',contxt)
    
#=============handles (location) coordinates storage and audit==
@login_required
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
@login_required
def ShowLoc(request):

    location = Location.objects.all()

    contxt = {
                   "locs":location
                }
    
    return render(request,"firstapp/location.html",contxt)

@login_required
def ShowTasks(request):

    tasks = Tasks.objects.all()

    contxt = { 
                  "tasks":tasks

                }

    return render(request,"firstapp/tasks.html",contxt)


# ==========initiate mpesa transaction (stk-push)==
@login_required
def MpesaTrans(request):
    if request.POST:
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")

        try:

            data = stk_push(phone,amount)
            if 'sales' in request.session:
                for key,value in request.session["sales"].items():
                    sales= Sales(
                        s_serial = request.session["sales"][key]["serial"],
                        s_name = request.session["sales"][key]["name"],
                        s_shop = Shops.objects.get(shop_id=request.session["sales"][key]["shops"] ),
                        s_qty = request.session["sales"][key]["qty"],
                        s_price = request.session["sales"][key]["price"],
                        s_cost = request.session["sales"][key]["cost"],
                        s_negatives = 0,
                        s_type= "mpesa",
                        s_profit = request.session["sales"][key]["profit"],
                        
                        s_created = datetime.now(),
                        s_creator = request.user
                    )
                    sales.save()
                    
                del request.session["sales"]
        
                return redirect('firstapp-counter')

        except:

            data = {"error":"failed"}

        return JsonResponse(data,status=200,safe=False)
    
 # ======== C 2 B register URL -- Daraja Api============
@csrf_exempt
def mpesa_reg_url(request):

    url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
    headers = { 'Authorization': f"Bearer {get_token()}"}

    req_body = {    
                   "ShortCode": "600980",
                   "ResponseType":"Completed",
                   "ConfirmationURL":os.getenv('conf_url'),
                   "ValidationURL":os.getenv('val_url'),
    }
    

    resp = requests.post(url,json=req_body,headers=headers)
    
    return JsonResponse(resp.json())

@csrf_exempt
def mpesa_sim(request):
    
    url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'

    headers = { 'Authorization': f"Bearer {get_token()}"}

    req_body = {
            "ShortCode":"600980",
    "CommandID": "CustomerPayBillOnline",
    "Amount": 1,
    "Msisdn": "254708374149",
    "BillRefNumber": "testapi",
    }

    response = requests.post(url,json=req_body,headers=headers)
    return JsonResponse(response.json())


@csrf_exempt
def c_2_b_conf_url(request):
     
    if request.method == "POST":
        try:
            data = request.body

            data = json.loads(data.decode('utf-8'))
            
            

            mpesa_res = mpesaPay(
                trans_id = data["TransID"],
                name=" ".join([data["FirstName"],data["MiddleName"],data["LastName"]]),
                phone = data["MSISDN"],
                ref_no = data["BillRefNumber"],
                amount = data["TransAmount"],
                details=str(data)
                )

            mpesa_res.save()
            
            resp = {
                "ResultCode": 0,
                "ResultDesc": "Accepted"
            }
            
            return JsonResponse(dict(resp))
        except:
            
            
            resp = {
                "ResultCode": 1,
                "ResultDesc": "failed"
            }
            
            return JsonResponse(dict(resp))
            
    
    return HttpResponse("waiting")
  
    
@csrf_exempt
def c_2_b_val_url(request):

    return HttpResponse("waiting")




    
# mpesa confirmation url

def MpesaConfirm(request):
    
    resp = request.body
    
    return HttpResponse(resp)

def postMpesaMessage(request):
    
    mpesa_rec = mpesaPay.objects.order_by('pk')
    #print(mpesa_rec)
    mpesa_rec = serializers.serialize('json',mpesa_rec)
    
    return JsonResponse(mpesa_rec,safe=False)
                    

def GenReceipt(request):
    
    sumqty = 0
    sumtot = 0

    if 'sales' in request.session:
        for key,val in request.session["sales"].items():
            
            sumqty += float(request.session["sales"][key]["qty"])
            sumtot += float(request.session["sales"][key]["price"])
           
    contxt = {"sumqty":sumqty,"sumtot":sumtot,"date":datetime.now(),"code":hash(datetime.now())}
    
    return render(request,'firstapp/receipt.html',contxt)

#========debt view point ====================

def DebtView(request):
    
    debts = Debts.objects.all()
    
    contxt ={"debts":debts}
    
    return render(request,'firstapp/debts.html',contxt)


#============handle debt register============

def DebtAdd(request):
    
    if request.POST:
        
        dname = request.POST.get("dname")
        dphone = request.POST.get("dphone")
        damount = request.POST.get("damount")
        dremks = request.POST.get("dremks")
        print(damount)
        try:
            debts = Debts(
                debt_cus = str(dname)+": "+str(dphone),
                debt_amnt = float(damount),
                debt_rem = float(damount),
                debt_last = datetime.now(),
                debt_remks = dremks,
                debt_creator = request.user
            )
        
            debts.save()
            
            mssg={"info":str(dname)+": "+str(dphone)+" "+str(damount)+" added successfully"}
            
        except Exception as e:
            print(e)
            
            mssg={"info":"failed to add debt"}
            
        return JsonResponse(mssg,status=200)
    
#============handle debt pay=============

def DebtPay(request):
    
    if request.POST:
        
        id = request.POST.get('ids')
        amount = request.POST.get("paid")
        
        try:
            
            debts_filt = Debts.objects.get(debt_id=int(id))
            debts_filt.debt_rem = debts_filt.debt_rem - float(amount)
            debts_filt.debt_last = datetime.now()
            
            debts_filt.save()
            
            mssg = {"info":"successfully paid"}
        
        except:
            
            
            mssg = {"info":"pay failed"}
            
        return JsonResponse(mssg,status=200)


    
# handles offline counter
def offline(request):
    
    return render(request,'firstapp/offline.html')

# 
def feeds_indexDB(request):

    products = Stocks.objects.all()
    products_json = serializers.serialize('json',products)
    return HttpResponse(products_json)

    
#============== error handling =============

# handle 404 error -> page not found

def error_404(request,exception):
    
    return render(request,'firstapp/404.html',status=404)

# handle 500 error -> error experiemced on server side

def error_500(request,exception=None):
    
    return render(request,'firstapp/500.html',status=500)


# handle 403 error -> permission denied , not authorised

def error_403(request,exception=None):
    
    return render(request,'firstapp/403.html',status=403)

