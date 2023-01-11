from django.urls import path
from . import views
from .views import StocksCreateView,ShopsCreateView,StocksUpdateView,ShopsListView,shopsUpdate
urlpatterns = [
    path('', views.home,name='firstapp-home'),
    path('counter/', views.counter,name='firstapp-counter'),
    path('getcounter', views.getCounter,name='firstapp-getcounter'),
    path('stocks/list',views.stocksView,name="firstapp-stocks"),
    path('shops/list',views.ShopsListView.as_view(),name="firstapp-shops"),
    path('shops/update',views.shopsUpdate,name="firstapp-updateshops"),
    path('stocks/addstocks/',StocksCreateView.as_view(),name="firstapp-addstocks"),
    path('stocks/<int:pk>/updates',StocksUpdateView.as_view(),name="firstapp-updatestocks"),
    path('addshops/',ShopsCreateView.as_view(),name="firstapp-addshops")
]