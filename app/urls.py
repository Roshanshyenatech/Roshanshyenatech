from django.contrib import admin
from django.urls import path

from app.views import password
from .views import register,login_user,password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',register.register_customer,name='register_customer'),
    path('login/',login_user.login_request,name='login_request'),
    path('reset/',password.reseting_password_request,name='reseting_password_request'),
    path('setpassword/',password.reseting_password_done,name='reseting_password_done'),
    path('changepassword/',password.change_password,name='change_password'),
    path('home/',login_user.home,name='home')
    ]
