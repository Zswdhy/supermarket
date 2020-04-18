from django.shortcuts import render, redirect, HttpResponse
from .models import User, Supplier, Bill
from .forms import Userform, Suppform, Billform
from django.http.response import JsonResponse
from supermarket.decorators import auth_seeion
from datetime import datetime
import pymysql


@auth_seeion
def userAdd(request):
    if request.method == "GET":
        return render(request, "userAdd.html")
    if request.method == "POST":
        f = Userform(request.POST)
        if f.is_valid():
            user = User.objects.filter(userName=f.instance.userName).first()
            if user:
                msg = "用户名已存在"
                return render(request, "userAdd.html", {"msg": msg})
            else:
                f.save()
                data = User.objects.all()
                return render(request, "userList.html", {"data": data})
        else:
            msg = "表单验证失败"
            return render(request, "userAdd.html", {"msg": msg})


@auth_seeion
def userList(requeste):
    if requeste.method == "GET":
        context = User.objects.all()
    if requeste.method == "POST":
        userName = requeste.POST.get("userName")
        context = User.objects.raw("select * from t_user where userName = %s", params=(userName,))
    return render(requeste, "userList.html", {"data": context})


@auth_seeion
def userUpdate(request, id):
    if request.method == "GET":
        data = User.objects.filter(id=id).first()
    if request.method == "POST":
        userName = request.POST.get("userName")
        sex = request.POST.get("sex")
        brith = request.POST.get("brith")
        tel = request.POST.get("tel")
        address = request.POST.get("address")
        userType = request.POST.get("userType")

        # 1、连接数据库
        conn = pymysql.connect(host="192.168.11.142", port=3306, user="root",
                               password="root", database="supermarket")
        # 2.通过conn连接，获取游标对象
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 3.通过游标对象操作数据库
        cursor.execute("UPDATE t_user SET userName= %s sex=%s  brith = %s tel=%s  address=%s userType=%s WHERE id = %s",
                       args=(userName, sex, brith, tel, address, userType, id))
        # 4.从缓冲区提交到数据库
        conn.commit()
        # 5.关闭资源
        cursor.close()
        return redirect("/res/userList")
    return render(request, "userUpdate.html", {"data": data})


@auth_seeion
def userViews(request):
    id = request.GET.get("id")
    data = User.objects.filter(id=id).first()
    return render(request, "userViews.html", {"data": data})


@auth_seeion
def providerAdd(request):
    if request.method == "GET":
        return render(request, "providerAdd.html")
    if request.method == "POST":
        f = Suppform(request.POST)
        if f.is_valid():
            supp = Supplier.objects.filter(suppId=f.instance.suppId).first()
            print(supp)
            if supp:
                msg = "供应商编号重复"
                return render(request, "providerAdd.html", {"msg": msg})
            else:
                f.instance.datetime = datetime.now()
                f.save()
                data = Supplier.objects.all()
                return render(request, "providerList.html", {"data": data})
        else:
            msg = "表单验证失败"
            return render(request, "billAdd.html", {"msg": msg})


@auth_seeion
def password(request):
    curpwd = request.POST.get("oldPassword")
    userid = request.session.get("loginFlag").get("id")
    oldpwd = User.objects.filter(id=userid).first().pwd
    newPassword = request.POST.get("newPassword")
    reNewPassword = request.POST.get("reNewPassword")

    if curpwd == oldpwd and reNewPassword == newPassword:
        # raw方式只能执行查询(select)语句,若使用修改，则需要用connect连接方式
        # 1.连接mysql服务器
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                               password="", database="supermarket")
        # 2.通过conn连接，获取游标对象
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 3.通过游标对象操作数据库
        cursor.execute("UPDATE t_user SET pwd = %s WHERE id = %s", args=(newPassword, userid))
        # 4.从缓冲区提交到数据库
        conn.commit()
        # 5.关闭资源
        cursor.close()
        return redirect(to='/')
    return render(request, "password.html")


@auth_seeion
def providerUpdate(request, id):
    if request.method == "GET":
        data = Supplier.objects.filter(id=id).first()
        return render(request, "providerUpdate.html", {"data": data})
    if request.method == "POST":
        suppId = request.POST.get("suppId")
        supplierName = request.POST.get("supplierName")
        linkman = request.POST.get("linkman")
        tel = request.POST.get("tel")
        addr = request.POST.get("addr")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        # raw方式只能执行查询(select)语句,若使用修改，则需要用connect连接方式
        # 1.连接mysql服务器
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                               password="", database="supermarket")
        # 2.通过conn连接，获取游标对象
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 3.通过游标对象操作数据库
        cursor.execute(
            "UPDATE t_supplier SET suppId=%s, supplierName= %s, linkman=%s, tel=%s,  addr = %s, email=%s, `desc`=%s  WHERE id = %s",
            args=(suppId, supplierName, linkman, tel, addr, email, desc, id))
        # 4.从缓冲区提交到数据库
        conn.commit()
        # 5.关闭资源
        cursor.close()
        return redirect('/res/providerList')
    return render(request, "providerUpdate.html")


@auth_seeion
def providerView(request):
    id = request.GET.get("id")
    data = Supplier.objects.filter(id=id).first()
    return render(request, "providerView.html", {"data": data})


@auth_seeion
def billAdd(request):
    if request.method == 'GET':
        supp = Supplier.objects.all().values("id", "supplierName")
        return render(request, "billAdd.html", {"data": supp})
    if request.method == 'POST':
        f = Billform(request.POST)
        if f.is_valid():
            # 查看订单编号是否存在
            bill = Bill.objects.filter(billId=f.instance.billId).first()
            if bill:
                msg = "订单编号已重复"
                supp = Supplier.objects.all().values("id", "supplierName")
                return render(request, "billAdd.html", {"data": supp, "msg": msg})
            # 保存数据
            supplier = request.POST.get("supplier")
            print(type(supplier))
            supplier = Supplier.objects.get(id=supplier)
            f.instance.supp = supplier
            f.instance.save()
            return redirect(to="/res/billList")
        else:
            return render(request, "billAdd.html", {"msg": "表单校验失败"})


@auth_seeion
def billList(request):
    supp = Supplier.objects.all().values("id", "supplierName")
    if request.method == "GET":
        context = Bill.objects.all()

    if request.method == "POST":
        name = request.POST.get("commodityName")
        supplier = request.POST.get("supplier")
        isPay = request.POST.get("isPay")
        if name != 'None' and supplier != 'None' and isPay != 'None':
            context = Bill.objects.raw("select * from t_bill where commodityName=%s and supp_id=%s and isPay=%s",
                                       params=(name, supplier, isPay))
            return render(request, "billList.html", {"data": context, "supplier": supp})

        context = Bill.objects.raw("select * from t_bill where commodityName=%s or supp_id=%s or isPay=%s",
                                   params=(name, supplier, isPay))

    return render(request, "billList.html", {"data": context, "supplier": supp})


@auth_seeion
def billUpdate(request, id):
    if request.method == "GET":
        supp = Supplier.objects.all().values("id", "supplierName")
        data = Bill.objects.filter(id=id).first()
        return render(request, "billUpdate.html", {"data": data, "supp": supp})
    if request.method == "POST":
        # id = request.POST.get("id")
        billId = request.POST.get("billId")
        commodityName = request.POST.get("commodityName")
        commodityUnit = request.POST.get("commodityUnit")
        commodityNum = request.POST.get("commodityNum")
        sumMoney = request.POST.get("sumMoney")
        supplier = request.POST.get("supplier")
        isPay = request.POST.get("isPay")
        # raw方式只能执行查询(select)语句,若使用修改，则需要用connect连接方式
        # 1.连接mysql服务器
        conn = pymysql.connect(host="192.168.11.142", port=3306, user="root",
                               password="root", database="supermarket")
        # 2.通过conn连接，获取游标对象
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 3.通过游标对象操作数据库
        cursor.execute(
            "UPDATE t_bill SET billId=%s, commodityName= %s, commodityUnit=%s, commodityNum=%s,  sumMoney = %s, supp_id=%s, isPay=%s  WHERE id = %s",
            args=(billId, commodityName, commodityUnit, commodityNum, sumMoney, supplier, isPay, id))
        # 4.从缓冲区提交到数据库
        conn.commit()
        # 5.关闭资源
        cursor.close()
        return redirect('/res/billList')


@auth_seeion
def billView(request):
    id = request.GET.get("id")
    data = Bill.objects.filter(id=id).first
    return render(request, "billView.html", {"data": data})


@auth_seeion
def providerList(request):
    if request.method == "GET":
        context = Supplier.objects.all()

    if request.method == "POST":
        name = request.POST.get("supplierName")
        context = Bill.objects.raw("select * from t_supplier where supplierName = %s ",
                                   params=(name,))
    return render(request, "providerList.html", {"data": context})


@auth_seeion
def logout(request):
    """
    退出系统并清除session
    :param request:
    :return:
    """
    request.session.flush()
    return redirect(to="/")


@auth_seeion
def index(request):
    userId = request.session.get("loginFlag").get("id")
    userName = User.objects.get(id=userId).userName
    return render(request, "index.html", {"userName": userName})


@auth_seeion
def deleteBill(request):
    id = request.GET.get("id")
    Bill.objects.get(id=id).delete()
    supp = Supplier.objects.all().values("id", "supplierName")
    context = Bill.objects.all()
    return render(request, "billList.html", {"data": context, "supp": supp})


@auth_seeion
def deleteSupp(request):
    id = request.GET.get("id")
    Supplier.objects.get(id=id).delete()
    context = Supplier.objects.all()
    return render(request, "providerList.html", {"data": context})


@auth_seeion
def deleteUser(request):
    id = request.GET.get("id")
    User.objects.get(id=id).delete()
    context = User.objects.all()
    return render(request, "userList.html", {"data": context})


def check(request):
    userId = request.GET.get("userId")
    tag = User.objects.filter(userId=userId).first()
    if tag:
        res = JsonResponse({"msg": '用户编号已存在！请重新输入！！！', "status": 0})
        res.setdefault("Access-Control-Allow-Origin", "*")
        return res
    else:
        res = JsonResponse({"msg": "用户名可用", "status": 0})
        res.setdefault("Access-Control-Allow-Origin", "*")
        return res


def checkpwd(request):
    newPassword = request.GET.get("newPassword")
    reNewPassword = request.GET.get("reNewPassword")
    if newPassword == reNewPassword:
        res = JsonResponse({"msg": '', "status": 0})
        res.setdefault("Access-Control-Allow-Origin", "*")
        return res
    else:
        res = JsonResponse({"msg": "密码不一致，请重新输入", "status": 0})
        res.setdefault("Access-Control-Allow-Origin", "*")
        return res
