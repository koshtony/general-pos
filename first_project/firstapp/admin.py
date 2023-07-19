from django.contrib import admin
from django.db.models import Sum
from .models import Stocks,Shops,Sales,Expenses,Transfers,Location,Tasks,Debts,Paid,mpesaPay


# Register your models here.

admin.site.register(Stocks)
admin.site.register(Shops)
admin.site.register(Sales)
admin.site.register(Expenses)
admin.site.register(Transfers)
admin.site.register(Location)
admin.site.register(Tasks)
admin.site.register(Debts)
admin.site.register(mpesaPay)

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
    
admin.site.register(Paid,PaidAdmin)