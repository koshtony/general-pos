"""first_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from posUsers import views as users_views # import users views direct
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',auth_view.LoginView.as_view(template_name='posUsers/login.html'),name="login"),
    path('logout/',auth_view.LoginView.as_view(template_name='posUsers/logout.html'),name="logout"),
    path('',include('firstapp.urls')),
    path('',include('posUsers.urls')),
    path('',include('smart_centre.urls'))

   # path('', include('pwa.urls')),

]

handler404 = "firstapp.views.error_404"
handler500 = "firstapp.views.error_500"
handler403 = "firstapp.views.error_403"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)


                 # default: "Django Administration"
admin.site.index_title = 'Admin page'                 # default: "Site administration"
admin.site.site_title = 'koshtech admin'