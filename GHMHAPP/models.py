from django.db import models

# Create your models here.
class UserInfo(models.Model):
    portrait = models.ImageField(upload_to='portrait', default='portrait.jpg', verbose_name='头像')
    user_name = models.CharField(max_length=32, verbose_name='用户名')
    account = models.CharField(max_length=32, verbose_name='账号', unique=True)
    password = models.CharField(max_length=32, verbose_name='密码')
    region = models.CharField(max_length=32, verbose_name='地区')
    #用户信息

class Mailbox(models.Model):
    userinfo = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name='用户')
    mailbox = models.CharField(max_length=32, verbose_name='邮箱')
    #用户邮箱

class School(models.Model):
    school = models.CharField(max_length=32, verbose_name='学校')
    #学校信息

class MH_PersonalDetail(models.Model):
    cover = models.ImageField(upload_to='cover', default='cover.jpg', verbose_name="封面")
    name = models.CharField(max_length=32, verbose_name='姓名')
    gender = models.CharField(max_length=2, verbose_name='性别', choices=(('1', '男'), ('2', '女')))
    age = models.CharField(max_length=32, verbose_name='年龄')
    region = models.CharField(max_length=32, verbose_name='地区')
    school = models.CharField(max_length=32, verbose_name='学校')
    contact = models.CharField(max_length=32, verbose_name='联系方式')
    introduction = models.TextField(verbose_name='个人简介')
    #盲盒信息

class Comment(models.Model):
    userinfo = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name='昵称')
    post = models.ForeignKey('MH_PersonalDetail', on_delete=models.CASCADE, verbose_name='盲盒')
    comment = models.TextField(verbose_name='评论')
    # 评论

class Comment_comment(models.Model):
    userinfo = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name='昵称')
    post = models.ForeignKey('Comment', on_delete=models.CASCADE, verbose_name='盲盒评论')
    comment = models.TextField(verbose_name='评论的评论')
    # 评论的评论