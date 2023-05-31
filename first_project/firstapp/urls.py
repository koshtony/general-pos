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
                StocksInbound, StocksTransfer,HandleLoc,ShowLoc,\
                ShowTasks,SalesReturn,MpesaTrans,GenReceipt,DebtAdd,DebtView,DebtPay, financeSummary,\
                    offline,feeds_indexDB,mpesa_reg_url,c_2_b_conf_url,c_2_b_val_url,cashier
            
urlpatterns = [

                    path('home', views.home,name='firstapp-home'),
                    path('counter/', views.counter,name='firstapp-counter'),
                    path('cashier/', views.cashier,name='firstapp-cashier'),
                    path('getcounter', views.getCounter,name='firstapp-getcounter'),
                    path('counter/plus', views.counterPlusSess,name='firstapp-counterplus'),
                    path('counter/minus', views.counterMinusSess,name='firstapp-counterminus'),
                    path('counter/remove', views.counterRemvSess,name='firstapp-counterremove'),
                    path('counter/mpesa', views.MpesaTrans,name='firstapp-stkpush'),
                    path('addsales', views.addSales,name='firstapp-addsales'),
                    path('reports/charts', views.Charts,name='firstapp-charts'),
                    path('sales/list',views.SalesListView.as_view(),name="firstapp-sales"),
                    path('sales/post',views.salesPostView,name="firstapp-salespost"),
                    path('sales/return',views.SalesReturn,name="firstapp-salesreturn"),
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
                    path('finance-summary',views.financeSummary,name="firstapp-financesummary"),
                    path('shops/update',views.shopsUpdate,name="firstapp-updateshops"),
                    path('stocks/addstocks/',StocksCreateView.as_view(),name="firstapp-addstocks"),
                    path('stocks/<int:pk>/updates',StocksUpdateView.as_view(),name="firstapp-updatestocks"),
                    path('addshops/',ShopsCreateView.as_view(),name="firstapp-addshops"),
                    path('location/', views.HandleLoc,name='firstapp-location'),
                    path('location/list', views.ShowLoc,name='firstapp-locationlist'),
                    path('tasks/list', views.ShowTasks,name='firstapp-taskslist'),
                    path('tasks/list', views.ShowTasks,name='firstapp-taskslist'),
                    path('counter/receipt', views.GenReceipt,name='firstapp-receipt'),
                    path('counter/debt', views.DebtAdd,name='firstapp-debt'),
                    path('debtlist', views.DebtView,name='firstapp-debtlist'),
                    path('debtpay', views.DebtPay,name='firstapp-debtpay'),
                    path('offline', views.offline,name='firstapp-offline'),
                    path('feeds_indexDB',views.feeds_indexDB,name="feeds-indexDB"),
                    path('register_url',views.mpesa_reg_url,name="register-url"),
                    path('conf_url',views.c_2_b_conf_url,name="conf-url"),
                    path('validate_url',views.c_2_b_val_url,name="validate-url")


]

