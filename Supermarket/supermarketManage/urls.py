from django.urls import path
from . import views

urlpatterns = [
    path("index", views.index),

    path("userAdd", views.userAdd),
    path("userList", views.userList),
    path("userViews", views.userViews),
    path("userUpdate/<int:id>", views.userUpdate),

    path("billAdd", views.billAdd),
    path("billList", views.billList),
    path("billUpdate/<int:id>", views.billUpdate),
    path("billView", views.billView),

    path("providerAdd", views.providerAdd),
    path("providerList", views.providerList),
    path("providerUpdate/<int:id>", views.providerUpdate),
    path("providerView", views.providerView),

    path("check", views.check),
    path("checkpwd", views.checkpwd),
    path("password", views.password),
    path("logout", views.logout),
    path("deleteBill", views.deleteBill),
    path("deleteSupp", views.deleteSupp),
    path("deleteUser", views.deleteUser),
]
