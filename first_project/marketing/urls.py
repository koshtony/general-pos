from django.urls import path
from . import views 
from .views import market_home,sys_message,unsaved_one_msg,unsaved_mult_msg,del_all_contacts

urlpatterns = [

    path('home_market/',views.market_home,name='market_home'),
    path('sys_msg/',views.sys_message,name='sys_msg'),
    path('unsaved_one_msg/',views.unsaved_one_msg,name='unsaved_one_msg'),
    path('unsaved_mult_msg/',views.unsaved_mult_msg,name='unsaved_mult_msg'),
    path('del_contacts/',views.del_all_contacts,name='del_contacts'),
]
