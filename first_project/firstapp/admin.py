from django.contrib import admin
from .models import Stocks,Shops,Sales,Expenses,Transfers,Location,Tasks

# Register your models here.

admin.site.register(Stocks)
admin.site.register(Shops)
admin.site.register(Sales)
admin.site.register(Expenses)
admin.site.register(Transfers)
admin.site.register(Location)
admin.site.register(Tasks)