"""
URL configuration for sever project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.urls import path, include

import file
from file import views
from sever import settings


def index(request):
    return render(request, "index.html")


def download(request,k):
    return FileResponse(open(settings.BASE_DIR / "static" / f"cloud-{k}.zip", "rb"))





urlpatterns = [
    path("", index),
    path("index", index),
    path("download/<str:k>", download),
    path(r'mdeditor/', include('mdeditor.urls')),
    path("admin/", admin.site.urls),
    path("api/account/", include("account.urls")),
    path("api/file/", include("file.urls")),
    path("api/upload/", include("upload.urls")),
    path("api/download/", include("download.urls")),
    path("api/pay/", include("pay.urls")),
    path("share/", include("sharefile.urls")),
    path("preview/<str:k>", views.preview),
    path("data/<str:k>", views.data),

]
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if "debug_toolbar" in settings.INSTALLED_APPS:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
