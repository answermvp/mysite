from django.db import models
from django.contrib.auth.models import User # 导入django自带的用户模型
from django.contrib.contenttypes.fields import GenericRelation # 反向关联
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType # 导入 ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod,ReadDetail


class BlogType(models.Model):
    '''博文类型模型'''
    # 类型名称
    type_name = models.CharField(max_length=15)

    def __str__(self):
        '''这个方法用来定义模型中的属性在后台显示成什么名称'''
        # 显示成 type_name
        return self.type_name 


class Blog(models.Model, ReadNumExpandMethod):
    '''博文模型'''
    # 博客标题
    title = models.CharField(max_length=50)
    # 博文类型，外键，关联到 BlogType 模型，删除博文的时候，不关联删除博文类型
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    # 博客内容，长文本格式
    content = RichTextUploadingField()
    # 博文作者，外键，关联到 User 模型，在做删除博文操作的时候，不关联删除博文的作者
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 通过contenttype的GenericRelation反向关联对应的模型
    read_details = GenericRelation(ReadDetail)
    # 阅读计数
    readed_num = models.IntegerField(default=0)
    # 创建时间，当做新增操作的时候，自动添加当前时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 最后更新时间，自动更新为当前时间
    last_updated_time = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk':self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-create_time']
        
        
