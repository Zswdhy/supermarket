from django.shortcuts import redirect


def auth_seeion(func):
    def check_session(request,*args, **kwargs):
        #1、获取session ，判断 session 是否有标识符
        dicts = request.session.get("loginFlag")
        if not dicts:
            return redirect(to="/")
        # 重置session 的存活时间
        request.session.set_expiry(30*60)
        # 清除过期的session
        request.session.clear_expired()
        return func(request, *args, **kwargs)
    return check_session