from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class LikeCount(models.Model):
    """点赞总数"""
    # 被点赞的对象
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # 点赞总数
    liked_num = models.IntegerField(default=0)

class LikeRecord(models.Model):
    """点赞记录"""
    # 被点赞的对象
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 点赞对象
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 点赞时间
    liked_time = models.DateTimeField(auto_now_add=True)