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
                    offline,feeds_indexDB,mpesa_reg_url,c_2_b_conf_url,c_2_b_val_url,mpesa_sim,\
                        cashier,addPaid,addContact,getContact,sendSms,postMpesaMessage,scanCounter,\
                            simple_counter,add_to_cart,del_cart_item,search_by_scan,search_by_name,search_by_category,\
                                search_by_desc,print_cart_receipt,cart_to_sales,clear_cart,transfer_data
            
urlpatterns = [

                    path('', views.home,name='firstapp-home'),
                    path('counter/', views.counter,name='firstapp-counter'),
                    path('cashier/', views.cashier,name='firstapp-cashier'),
                    path('getcounter', views.getCounter,name='firstapp-getcounter'),
                    path('scancounter', views.scanCounter,name='firstapp-scancounter'),
                    path('counter/plus', views.counterPlusSess,name='firstapp-counterplus'),
                    path('counter/minus', views.counterMinusSess,name='firstapp-counterminus'),
                    path('counter/remove', views.counterRemvSess,name='firstapp-counterremove'),
                    path('counter/mpesa', views.MpesaTrans,name='firstapp-stkpush'),
                    path('addsales', views.addSales,name='firstapp-addsales'),
                    path('addpaid', views.addPaid,name='firstapp-addpaid'),
                    path('addcontact', views.addContact,name='firstapp-addcontact'),
                    path('getcontact', views.getContact,name='firstapp-getcontact'),
                    path('sendsms', views.sendSms,name='firstapp-sendsms'),
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
                    path('validate_url',views.c_2_b_val_url,name="validate-url"),
                    path('mpesa_sim',views.mpesa_sim,name="mpesa-sim"),
                    path('mpesa_msg',views.postMpesaMessage,name="mpesa-msg"),
                    
                    
                    # simple counter 
                    path("simple_counter/",views.simple_counter,name="simple-counter"),
                    path("add_to_cart/<int:id>/",views.add_to_cart,name="add-to-cart"),
                    path('update_cart_qty/<int:id>/',views.update_cart_qty,name="update-cart-qty"),
                    path('del_cart_item/<int:id>/',views.del_cart_item,name="del-cart-item"),
                    path('search_by_scan',views.search_by_scan,name="search-by-scan"),
                    path('search_by_name',views.search_by_name,name="search-by-name"),
                    path('search_by_category',views.search_by_category,name="search-by-category"),
                    path('search_by_desc',views.search_by_desc,name="search-by-desc"),
                    path('print_cart_receipt',views.print_cart_receipt,name='print-cart-receipt'),
                    path('cart_to_sales/',views.cart_to_sales,name="cart-to-sales"),
                    path('clear_cart/',views.clear_cart,name="clear-cart"),
                    path('transfer_data/',views.transfer_data,name="transfer-data"),
                    
                    
                    


]

