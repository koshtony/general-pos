from django.urls import path
from . import views
from .views import StocksCreateView,\
    ShopsCreateView,StocksUpdateView,\
    ShopsListView,shopsUpdate,\
    addSales,SalesListView,Charts,\
    OrdersView,InvoiceView,financeView,\
        financePostView,financeUpdateView,\
            stocksPostView,salesPostView,\
                counterPlusSess,counterMinusSess,counterRemvSess,\
                StocksInbound, StocksTransfer
            
urlpatterns = [
    path('', views.home,name='firstapp-home'),
    path('counter/', views.counter,name='firstapp-counter'),
    path('getcounter', views.getCounter,name='firstapp-getcounter'),
    path('counter/plus', views.counterPlusSess,name='firstapp-counterplus'),
    path('counter/minus', views.counterMinusSess,name='firstapp-counterminus'),
    path('counter/remove', views.counterRemvSess,name='firstapp-counterremove'),
    path('addsales', views.addSales,name='firstapp-addsales'),
    path('reports/charts', views.Charts,name='firstapp-charts'),
    path('sales/list',views.SalesListView.as_view(),name="firstapp-sales"),
    path('sales/post',views.salesPostView,name="firstapp-salespost"),
    path('stocks/list',views.stocksView,name="firstapp-stocks"),
    path('stocks/post',views.stocksPostView,name="firstapp-stockspost"),
    path('stocks/inbound',views.StocksInbound,name="firstapp-stocksinbound"),
    path('stocks/transfer',views.StocksTransfer,name="firstapp-stockstransfer"),
    path('shops/list',views.ShopsListView.as_view(),name="firstapp-shops"),
    path('orders/list',views.OrdersView,name="firstapp-orders"),
    path('invoice',views.InvoiceView,name="firstapp-invoice"),
    path('finance',views.financeView,name="firstapp-finance"),
    path('finance-add',views.financePostView,name="firstapp-financeadd"),
    path('finance-update',views.financeUpdateView,name="firstapp-financeupdate"),
    path('shops/update',views.shopsUpdate,name="firstapp-updateshops"),
    path('stocks/addstocks/',StocksCreateView.as_view(),name="firstapp-addstocks"),
    path('stocks/<int:pk>/updates',StocksUpdateView.as_view(),name="firstapp-updatestocks"),
    path('addshops/',ShopsCreateView.as_view(),name="firstapp-addshops")
]