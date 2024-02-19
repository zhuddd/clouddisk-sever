from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login),
    path("register", views.register),
    path("captcha", views.get_captcha),
    path("update_password", views.update_password),
    ]