from django.shortcuts import get_object_or_404, render
# 导入分页器类
from django.core.paginator import Paginator
from django.conf import settings
# 导入计数方法，供annotate使用
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read
import markdown

# Create your views here.


def get_blog_list_common_data(request, blogs_all_list):
    '''获取博客列表公共数据'''
    # 用分页器分页，每页显示几条博客
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    # 获取请求中的页码参数
    page_num = request.GET.get('page', 1)
    # 某一页的所有博客
    page_of_blogs = paginator.get_page(page_num)
    # 获取当前页码
    current_page_num = page_of_blogs.number
    # 获取当前页的前两页到当前页的后两页的页码范围
    page_range = list(range(max(current_page_num -2, 1), current_page_num)) + \
    list(range(current_page_num, min(current_page_num + 2 , paginator.num_pages)+ 1))
    # 省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0,'...') # 下标0处插入省略号
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    #  加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0 ,1) # 下标0处插入1
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类对应的博客数量
    '''
    通过annotate给模型对象添加注释
        BlogType.objects.annotate(blog_count=Count('blog')) 
            这里是为BlogType模型的对象添加blog_count注释
            Count('blog)中的blog是BlogType的关联模型BLOG的小写
    
    笨方法
    blog_types = BlogType.objects.all()#所有博客分类，QuerySet
    blog_types_list = []
    for blog_type in blog_types:#其中一个博客分类，BlogType类的一个对象
        # blog_count = Blog.objects.filter(blog_type=blog_type).count()其中一个分类的博客数量
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()#给对象添加一个属性
        blog_types_list.append(blog_type)
    '''
    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('create_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,
                                         create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    # 某一页的所有博客传到前端页面
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog')) # 所有博文类型
    # 获取博客创建时间分类：将创建时间按月分类，倒序
    # context['blog_dates'] = Blog.objects.dates('create_time', 'month', order="DESC")
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    '''博客列表'''
    blogs_all_list = Blog.objects.all() #获取所有博客
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context) # 渲染并返回前端页面


def blogs_with_type(request, blog_type_pk):
    '''博文所属分类模型，返回同类型的所有博文'''
    # 根据博文类型主键（id）获取对应的博文类型，没有结果则返回404
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type) # 获取所有同类博客
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    '''按照创建日期分类'''
    blogs_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blogs_with_date.html', context)


def blog_detail(request, blog_pk):
    '''博客详情'''
    # 根据博文的主键（id）获取对应的博文，如果没有结果则自动返回404
    blog = get_object_or_404(Blog, pk=blog_pk) 
    # 调用阅读计数方法
    read_cookie_key = read_statistics_once_read(request, blog)

    context = {}
    # 通过创建时间大于当前博客的最后一条，获取的当前博客的上一篇博客
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    # 通过创建时间小于当前博客的第一条，获取当前博客的下一篇博客
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    blog.content = markdown.markdown(blog.content,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])
    context['blog'] = blog
    response = render(request, 'blog/blog_detail.html', context) # 响应
    # 设置cookie记录是否读过blog
    response.set_cookie(read_cookie_key, 'True')
    return response