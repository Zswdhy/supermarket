from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.login),
    path("res/", include("supermarketManage.urls")),
    # path("<slug:path>", views.path)
]
