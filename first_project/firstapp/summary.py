from django.db.models import Sum
from django.db.models.functions import TruncMonth
from posUsers.models import Profile
from .models import Shops
from datetime import datetime, timedelta,date

def sales_summ(object):
    labels,profit,qty = [],[],[]
    
    
    sales  = object.objects.values('s_name').annotate(total_profit= Sum('s_profit'),total_qty= Sum('s_qty'))

    for sale in sales:
        labels.append(sale["s_name"])
        profit.append(sale["total_profit"])
        qty.append(sale["total_qty"])
        
    return labels,profit,qty
        
        
def stocks_summ(object):
    
    labels,cost,price,qty  = [],[],[],[]
    
    stocks = object.objects.values('p_name').annotate(total_cost= Sum('p_cost'),total_price= Sum('p_price'),total_qty = Sum('p_qty'))
    
    for stock in stocks:
        
        labels.append(stock["p_name"])
        cost.append(stock["total_cost"])
        price.append(stock["total_price"])
        qty.append(stock["total_qty"])
        
    return labels,cost,price,qty

def time_sales_summ(object):
    
    dates,qty,profit = [],[],[]
    
    objs = object.objects.annotate(month=TruncMonth('s_created')).values('month').annotate(sum_qty=Sum('s_profit'))
    
    for obj in objs:
        
        dates.append(obj["month"])
        qty.append(obj["sum_qty"])
        
    return dates,qty
        

def sales_summary(object):
    all_sales = []
    sales = object.objects.all()
    
    for sale in sales:
        
        all_sales.append(
            
            {
                "shop":sale.s_shop.shop_name,
                "product":sale.s_name,
                "qty": sale.s_qty,
                "revenue": sale.s_price,
                "profit":sale.s_profit,
                "expense":0,
                "Date": sale.s_created,
                
                
                
                
            }
            
            
        )
    return all_sales

def exp_summary(object):
    
    all_exp = []
    
    exps = object.objects.all()
    
    for exp in exps:
        
        all_exp.append({
            
            "shop":exp.exp_shop,
            "product":"expense",
            "qty": 0,
            "revenue":0,
            "profit":0,
             "expense":exp.exp_amount,
            "Date": exp.exp_date,
            
        })
        
    return all_exp
    
def today_summary(model1,model2):
    tmrrw = datetime.now()+timedelta(1)
    tmrrw = datetime.strftime(tmrrw, '%Y-%m-%d')
    ystdy = datetime.now()
    ystdy = datetime.strftime(ystdy, '%Y-%m-%d')
    today_paid = model1.objects.filter(s_created__range=[ystdy,tmrrw])
    today_sales = model2.objects.filter(s_created__range=[ystdy,tmrrw])
    
    today_profit = [paid.s_profit for paid in today_paid]
    today_sales = [sale.s_qty for sale in today_sales]
    today_amount = [paid.s_price for paid in today_paid]
    return sum(today_profit),sum(today_sales),sum(today_amount)

    
def monthly_comp(sales,stocks):

    sales_ = sales.objects.filter(s_created__range=[date.today()-timedelta(datetime.now().day),date.today()]).values("s_name").annotate(total_qty=Sum('s_qty'))
    seller = sales.objects.values('s_creator').annotate(total_sales=Sum('s_qty'))
    shops = sales.objects.values('s_shop').annotate(total_sales=Sum('s_qty'))
    stocks = stocks.objects.values("p_name").annotate(total_stock=Sum('p_qty'))
    print(stocks)
    stock_names =[stock["p_name"] for stock in stocks]
    print(stock_names)
    stock_qty = [stock["total_stock"] for stock in stocks]
    sales_qty = [sale["total_qty"] for sale in sales_]
    seller_qty = [sell["total_sales"] for sell in seller]
    seller_user = [Profile.objects.get(user=sell["s_creator"]).user.username for sell in seller]
    shop_qty = [shop["total_sales"] for shop in shops]
    shop_name = [Shops.objects.get(shop_id=shop["s_shop"]).shop_name for shop in shops]

    return stock_names,stock_qty,sales_qty,seller_qty,seller_user,shop_qty,shop_name



        