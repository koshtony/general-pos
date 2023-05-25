from django.shortcuts import render
from firstapp.models import Stocks,Sales,Shops
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from datetime import datetime
# handles offline counter
@login_required
def offline_counter(request):
    
    return render(request,'offline_pos/off_counter.html')

@login_required
def offline_sales(request):

    return render(request,'offline_pos/off_sale.html')

@login_required
def commit_sales(request):

    if request.POST:
        ids = request.POST.get("id")
        receipt = request.POST.get("receipt")
        qty = request.POST.get("qty")


        stoks2 = Stocks.objects.get(p_id=ids)
        stoks = Stocks.objects.get(p_id=ids)
        stoks.p_qty = stoks2.p_qty - int(qty)
        stoks.save()

        new_sale = Sales(

             s_serial = receipt,
             s_name = stoks2.p_name,
            s_shop = Shops.objects.get(shop_id=9) ,
            s_qty = qty,
            s_price = stoks2.p_price,
            s_cost = stoks2.p_cost,
            s_negatives = 0,
            s_profit = (int(qty)*float(stoks2.p_price))-(int(qty)*stoks2.p_cost),
            s_created = datetime.now(),
            s_creator = request.user


            )
        new_sale.save()

        return JsonResponse("sale successfully committed online",safe=False)
# 
def feeds_indexDB(request):

    products = Stocks.objects.all()
    products_json = serializers.serialize('json',products)
    return HttpResponse(products_json)
