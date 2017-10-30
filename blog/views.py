from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from .models import Post, Category
import markdown
from comments.forms import CommentForm

'''
def index(request):
	#return HttpResponse('hello world')
	return render(request, 'blog/index.html', context={
					'title': '我的博客首页',
					'welcome': "欢迎"
				})
'''
'''
def index(request):
	#博客首页
	post_list = Post.objects.all().order_by('-created_time')
	return render(request, 'blog/index.html', context={'post_list': post_list})
'''
#用类视图类替换index视图,这个类等价于index函数
from django.views.generic import ListView
class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 2  #设置分页功能，每页显示两篇文章
'''
def detail(request,pk):
	#文章详情页
	post = get_object_or_404(Post, pk=pk)
	#设置markdown语法
	post.body = markdown.markdown(post.body,extensions=['markdown.extensions.extra','markdown.extensions.codehilite','markdown.extensions.toc',])
	return render(request, 'blog/detail.html', context={'post':post})
'''
#更新文章详情页视图，添加评论信息
def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	#阅读量加1
	post.increase_views()
	post.body = markdown.markdown(post.body,extensions=['markdown.extensions.extra','markdown.extensions.codehilite','markdown.extensions.toc',])
	form = CommentForm()
	comment_list = post.comment_set.all()
	context = {'post':post,'form':form,'comment_list':comment_list}
	return render(request, 'blog/detail.html',context=context)

#因为日期归档页和标签分类页显示效果和首页相同，所以render的模板为index.html
#归档页
def archives(request, year, month):
	#按日期归档页，不同的月份的文章显示到不同的页
	post_list = Post.objects.filter(created_time__year=year,created_time__month=month).order_by('-created_time')
	return render(request, 'blog/index.html', context={'post_list': post_list})
#分类页
'''
def category(request, pk):
	cate = get_object_or_404(Category, pk=pk)
	post_list = Post.objects.filter(category=cate).order_by('-created_time')
	return render(request, 'blog/index.html', context={'post_list': post_list})
'''
#使用类视图改写category视图函数
class CategoryView(ListView):
	model = Post 
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	
	def get_qyeryset(self):
		cate = get_objet_or_404(Category, pk=self.kwargs.get('pk'))
		return super(CategoryView, self).get_queryset().filter(category=cate)
