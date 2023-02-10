from django.db.models import Sum

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