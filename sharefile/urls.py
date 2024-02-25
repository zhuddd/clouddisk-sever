from django.urls import path
from . import views

urlpatterns = [
    # path("filedir/<int:t>/<str:msg>", views.filedir),
    path("new", views.newShare),
    path("get/<str:code>", views.getShare),
    path("save", views.shareSave),
    path("list", views.shareList),
    path("delete", views.shareDelete),

]
