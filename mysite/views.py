import datetime
from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.urls import reverse # 导入反向解析
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog

def get_7_days_hot_blogs():
    """返回7天热门博客"""
    # 当前日期
    today = timezone.now().date()
    # 前7天日期
    date = today - datetime.timedelta(days=7)
    # 通过过滤，分组，聚合，排序获取7天热门博客
    blogs = Blog.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    '''首页'''
    # 通过 ContentType 找到 Blog 模型
    blog_content_type = ContentType.objects.get_for_model(Blog)
    # 调用 get_seven_days_read_data 方法拿到7天阅读数列表和7天的日期
    dates,read_nums = get_seven_days_read_data(blog_content_type)
    # 调用 get_today_hot_data 方法获取到当天热门博客
    # today_hot_data = get_today_hot_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days') # 获取缓存
    if hot_blogs_for_7_days is None: # 如果返回结果为None, 说明数据库中没有缓存
        hot_blogs_for_7_days = get_7_days_hot_blogs() # 获取数据
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600) # 将获取到的数据设置到缓存
    

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = get_7_days_hot_blogs()
    return render(request,'home.html', context)

