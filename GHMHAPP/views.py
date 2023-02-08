from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from GHMHAPP import models
from django.core import mail
import random

# Create your views here.

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        login_account = request.POST.get('login_account')
        login_password = request.POST.get('login_password')
        try:
            user = models.UserInfo.objects.get(account=login_account)
        except models.UserInfo.DoesNotExist:
            messages.error(request, '用户不存在')
            return render(request, 'index.html')
        user_passward = user.password
        if login_password != user_passward:
            messages.error(request, '密码错误')
            return render(request, 'index.html')
        else:
            request.session['user_name'] = user.user_name
            request.session['account'] = user.account
            request.session.set_expiry(0)
            messages.error(request, '登录成功')
            return render(request, 'index.html')
def flush(request):
    request.session.flush()
    messages.error(request, '已登出')
    return HttpResponseRedirect('/')
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        account = request.POST.get('register_account')
        mailbox = request.POST.get('register_mailbox')
        password = request.POST.get('register_password')
        re_password = request.POST.get('register_re_password')
        verification_code_input = request.POST.get('register_verification_code_input')
        verification_code = request.session.get('verification_code')
        if re_password != password:
            messages.error(request, '密码不一致')
            return render(request, 'register.html')
        elif verification_code == '':
            messages.error(request, '验证码已过期')
            return render(request, 'register.html')
        elif verification_code_input != verification_code:
            messages.error(request, '请输入正确的验证码')
            return render(request, 'register.html')
        else:
            try:
                models_account = models.UserInfo.objects.get(account=account).account
            except models.UserInfo.DoesNotExist:
                models_account = ''
            if models_account == account:
                messages.error(request, '用户名已存在')
                return render(request, 'register.html')
            else:
                models.UserInfo.objects.create(user_name=account, account=account, password=password)
                models.Mailbox.objects.create(userinfo=models.UserInfo.objects.get(account=account), mailbox=mailbox)
                messages.error(request, '注册成功')
            return HttpResponseRedirect('/')
def mailbox(request):
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWSYZ'
    verification_code = ''
    mailbox = request.POST.get('mailbox')
    for x in range(4):
        verification_code += random.choice(chars)
    mail.send_mail(
        subject='你的验证码',  # 题目
        message='欢迎使用盲盒，为保证您的正常使用，请输入下面的验证码\n' + verification_code + '\n注意：验证码的有效期为30分钟',  # 消息内容
        from_email='2228795091@qq.com',  # 发送者[当前配置邮箱]
        recipient_list=[mailbox],  # 接收者邮件列表
    )
    request.session['verification_code'] = verification_code
    request.session.set_expiry(1800)
    messages.error(request, '已发送')
    return render(request, 'mailbox.html')
def user_detail(request):
    user = models.UserInfo.objects.get(account=request.session.get('account'))
    return render(request, 'user_detail.html', {'user': user})
def user_collection(request):
    return render(request, 'user_collection.html')
def place(request):
    return render(request, 'place.html')
def extract(request):
    school = models.School.objects.all()
    if request.method == 'GET':
        return render(request, 'extract.html', {'school': school})
    if request.method == 'POST':
        select_school = request.POST.get('select_school')
        select_gender = request.POST.get('select_gender')
        if select_school == '0':
            if select_gender == '0':
                mh_personal_detail = models.MH_PersonalDetail.objects.all().order_by("?").first()
            else:
                mh_personal_detail = models.MH_PersonalDetail.objects.filter(select_gender=select_gender).order_by(
                    "?").first()
        else:
            if select_gender == '0':
                mh_personal_detail = models.MH_PersonalDetail.objects.filter(school=select_school).order_by("?").first()
            else:
                mh_personal_detail = models.MH_PersonalDetail.objects.filter(school=select_school,
                                                                             gender=select_gender).order_by(
                    "?").first()
            try:
                user = models.UserInfo.objects.get(account=request.session.get("account"))
            except models.UserInfo.DoesNotExist:
                user = ''
            if user != '' and mh_personal_detail is not None:
                try:
                    models.Boxid.objects.get(user=user, boxdetail=mh_personal_detail)
                except models.Boxid.DoesNotExist:
                    models.Boxid.objects.create(user=user, boxdetail=mh_personal_detail)
            personal_detail_comment = models.Comment.objects.filter(post=mh_personal_detail)
            return render(request, 'extract.html', {'mh_personal_detail': mh_personal_detail, 'school': school})





"""盲盒"""
def mh(request):
    return render(request, 'mh.html')
def mh_detail(request):
    return render(request, 'user_detail.html')
def mh_forum(request):
    return render(request, 'mh_forum.html')