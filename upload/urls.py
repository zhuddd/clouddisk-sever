from django.urls import path
from upload import views

urlpatterns = [
    path("upload", views.upload_view),
    path("creat_contents", views.creat_contents),
    ]