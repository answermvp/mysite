import datetime
from django.contrib.contenttypes.models import ContentType # 导入 ContentType
from django.utils import timezone
from django.db.models import Sum # 导入聚合函数
from .models import ReadNum, ReadDetail

def read_statistics_once_read(request, obj):
    '''阅读计数方法'''
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    # 如果请求中没有名称为“读过”的cookie
    if not request.COOKIES.get(key):
        # 存在则获取，不存在则创建，返回列表，如果是获取的，created 值为 false
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # 总阅读数加一
        readnum.read_num += 1
        readnum.save()

        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        # 给当天的阅读统计中阅读数也加一
        readDetail.read_num += 1
        readDetail.save()
    return key

def get_seven_days_read_data(content_type):
    """返回最近7天的阅读数"""
    # 当前日期
    today = timezone.now().date()
    # 7天的日期
    dates = []
    # 7天的阅读数列表
    read_nums = []
    for i in range(7, 0, -1):
        # 7天中每一天的日期
        date = today - datetime.timedelta(days=i)
        # 每天的日期添加到列表
        dates.append(date.strftime('%m/%d'))
        # 每天的阅读数
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        # 对每天的阅读数聚合，返回字典
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        # 每天的阅读数添加到填表，如果是 none/false 则转成 0
        read_nums.append(result['read_num_sum'] or 0)
    # 返回阅读数列表
    return dates,read_nums

def get_today_hot_data(content_type):
    """返回当天热门阅读博客"""
    # 当前日期
    today = timezone.now().date()
    # 对当天的博客通过阅读数倒序排序
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7] # 最多取7条

def get_yesterday_hot_data(content_type):
    """返回昨天热门阅读博客"""
    # 当前日期
    today = timezone.now().date()
    # 昨天日清
    yesterday = today - datetime.timedelta(days=1)
    # 对昨天的博客通过阅读数倒序排序
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]
