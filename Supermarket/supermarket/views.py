from django.shortcuts import render, redirect
from supermarketManage.models import User
from supermarket.decorators import auth_seeion


def path(request, path):
    return render(request, f"{path}.html")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        userName = request.POST.get("userName")
        pwd = request.POST.get("pwd")
        user = User.objects.filter(userName=userName).first()
        if not user:
            return render(request, "login.html", {"msg": "用户不存在"})
        if pwd != user.pwd:
            return render(request, "login.html", {"msg1": "密码错误"})

        # 存储用户登陆成功的标识，该标识存储在 session 会话中
        request.session["loginFlag"] = {"id": user.id, "userName": user.userName}
        return redirect('/res/index')


