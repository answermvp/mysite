import threading # 多线程
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey # 导入通用外键
from django.contrib.contenttypes.models import ContentType # 导入ContentType模型
from django.contrib.auth.models import User # 导入django自带的用户模型
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render


class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text
        )

# Create your models here.
class Comment(models.Model):
    """评论模型"""
    # 评论对象
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # 关联模型（Blog）
    object_id = models.PositiveIntegerField() # 所关联模型的主键id（具体哪一篇博客）
    content_object = GenericForeignKey('content_type', 'object_id')
    # 评论内容
    text = models.TextField()
    # 评论时间
    comment_time = models.DateTimeField(auto_now_add=True)
    # 评论者
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    # 记录回复是基于哪一条评论开始的
    root = models.ForeignKey('self', related_name="root_comment", null=True, on_delete=models.CASCADE)
    # 上一级 外键，关联自己
    parent = models.ForeignKey('self', related_name="parent_comment", null=True, on_delete=models.CASCADE)
    # 回复谁
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)

    def send_mail(self):
        # 发送邮件通知
        if self.parent is None:
            # 评论我的博客
            subject = '有人评论你的博客'
            email = self.content_object.get_email()
        else:
            # 回复评论
            subject = '有人回复你的评论'
            email = self.reply_to.email
        if email != '':
            context = {}
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render(None, 'comment/send_mail.html', context).content.decode('utf-8')
            send_mail = SendMail(subject, text, email)
            send_mail.start()
            

    def __str__(self):
        """返回评论内容"""
        return self.text



    class Meta:
        """评论时间倒序显示"""
        ordering = ['comment_time']
