from django.contrib import admin
from django.db.models import Sum
from .models import Stocks,Shops,Sales,Expenses,Transfers,Location,Tasks,Debts,Paid,mpesaPay,Cart


# Register your models here.


admin.site.register(Shops)
admin.site.register(Sales)
admin.site.register(Expenses)
admin.site.register(Transfers)
admin.site.register(Location)
admin.site.register(Tasks)
admin.site.register(Debts)
admin.site.register(Cart)
class StocksAdmin(admin.ModelAdmin):
    
    list_display = ('p_serial','p_name','p_category','p_qty','p_price','p_cost','p_vat','p_shop__shop_name','p_created','p_creator')
    list_filter = ("p_shop__shop_name",)
    search_fields = ("p_serial","p_name","p_category",)


class PaidAdmin(admin.ModelAdmin):
    
    list_display = ('sn','product','qty',"amount","profit",'waiter','date',)
    list_filter = ("waiter",)
    search_fields = ("sn",)
    
    list_summary = (('Total amount', Sum('tot_amount'), ),
                    ('Total Profit', Sum('tot_profit'), ))
   
    def get_queryset(self, request):
        return super(PaidAdmin, self).get_queryset(request).annotate(
            tot_amount=Sum('amount'),
            tot_profit=Sum('profit'))
        
class MpesaAdmin(admin.ModelAdmin):
    
    list_display = ('trans_id','name','phone',"ref_no","date",'amount',)
    list_filter = ("name",)
    search_fields = ("trans_id",)

admin.site.register(Paid,PaidAdmin)
admin.site.register(mpesaPay,MpesaAdmin)
admin.site.register(Stocks,StocksAdmin)