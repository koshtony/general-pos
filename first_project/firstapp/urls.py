from django.urls import path
from . import views
from .views import StocksCreateView,\
    ShopsCreateView,StocksUpdateView,\
    ShopsListView,shopsUpdate,\
    addSales,SalesListView,Charts,\
    OrdersView,InvoiceView,financeView
urlpatterns = [
    path('', views.home,name='firstapp-home'),
    path('counter/', views.counter,name='firstapp-counter'),
    path('getcounter', views.getCounter,name='firstapp-getcounter'),
    path('addsales', views.addSales,name='firstapp-addsales'),
    path('reports/charts', views.Charts,name='firstapp-charts'),
    path('sales/list',views.SalesListView.as_view(),name="firstapp-sales"),
    path('stocks/list',views.stocksView,name="firstapp-stocks"),
    path('shops/list',views.ShopsListView.as_view(),name="firstapp-shops"),
   path('orders/list',views.OrdersView,name="firstapp-orders"),
   path('invoice',views.InvoiceView,name="firstapp-invoice"),
   path('finance',views.financeView,name="firstapp-finance"),
    path('shops/update',views.shopsUpdate,name="firstapp-updateshops"),
    path('stocks/addstocks/',StocksCreateView.as_view(),name="firstapp-addstocks"),
    path('stocks/<int:pk>/updates',StocksUpdateView.as_view(),name="firstapp-updatestocks"),
    path('addshops/',ShopsCreateView.as_view(),name="firstapp-addshops")
]