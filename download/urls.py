from django.urls import path
from download import views

urlpatterns = [
    path("download", views.download),
    path("tree", views.get_tree),
    ]