from django.urls import path
from . import views

urlpatterns = [
    path('menu', views.getMenu),
    path('info', views.getInfo),
    path('pay', views.pay),
    path('paysuccess', views.paysuccess),
    path('callback', views.callback),
    path('admin', views.admin),
    path('income', views.income),
    ]