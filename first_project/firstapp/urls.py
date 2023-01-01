from django.urls import path
from . import views
from .views import StocksCreateView,ShopsCreateView
urlpatterns = [
    path('', views.home,name='firstapp-home'),
    path('counter/', views.counter,name='firstapp-counter'),
    path('stocks/',views.stocksView,name="firstapp-stocks"),
    path('addstocks/',StocksCreateView.as_view(),name="firstapp-addstocks"),
    path('addshops/',ShopsCreateView.as_view(),name="firstapp-addshops")
]