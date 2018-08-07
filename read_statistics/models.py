from django.db import models
from django.db.models.fields import exceptions # 导入异常处理
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class ReadNum(models.Model):
    """阅读计数模型"""
    read_num = models.IntegerField(default=0)
    # 通过ContentType关联模型
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 关联模型的主键
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExpandMethod():
    """返回阅读数"""
    def get_read_num(self):
            try:
                # 通过ContentType找到指定模型
                ct = ContentType.objects.get_for_model(self)
                # 获取指定模型指定主键id的查询对象
                readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
                # 获取阅读计数
                return readnum.read_num
            # 如果报不存在，返回0
            except exceptions.ObjectDoesNotExist:
                return 0

class ReadDetail(models.Model):
    """阅读记录详细信息"""
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)

    # 通过ContentType关联模型
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 关联模型的主键
    object_id = models.PositiveIntegerField()
    # 关联模型的对象
    content_object = GenericForeignKey('content_type', 'object_id')
