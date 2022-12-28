from django.urls import path
from . import views
from .views import StocksListViews,StocksCreateView
urlpatterns = [
    path('', views.home,name='firstapp-home'),
    path('counter/', views.counter,name='firstapp-counter'),
    path('stocks/',StocksListViews.as_view(),name="firstapp-stocks"),
    path('addstocks/',StocksCreateView.as_view(),name="firstapp-addstocks")
]