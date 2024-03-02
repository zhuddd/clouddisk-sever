from django.urls import path
from . import views

urlpatterns = [
    path("filedir/<int:t>/<str:msg>", views.filedir),
    path("folderlist", views.folderList),
    path("used", views.usedStorage),
    path("delete", views.delete),
    path("rename", views.rename),
    path("paste", views.paste),
    path("newfolder", views.newfolder),
    path('face/<str:k>/<str:t>', views.getface),
    path('getkey/', views.getPreviewKey),
    path("poster/<str:k>", views.poster),

    # path("uploadold", views.upload),
    # path("updir", views.updir),
    # path("setface", views.setfileface),

]
