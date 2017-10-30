from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse


@python_2_unicode_compatible
class Category(models.Model):
	'''
	创建分类数据库表
	'''
	name = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Tag(models.Model):
	'''
	创建标签数据库表
	'''
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Post(models.Model):
	'''
	创建文章数据库表
	'''
	title = models.CharField(max_length=70)
	body = models.TextField()
	created_time = models.DateTimeField()
	modified_time = models.DateTimeField()
	excerpt = models.CharField(max_length=200, blank=True)
	category = models.ForeignKey(Category)
	tags = models.ManyToManyField(Tag, blank=True)
	author = models.ForeignKey(User)
	views = models.PositiveIntegerField(default=0)
	
	#浏览量自增
	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])
	
	#save方法从文章中提取摘要
	import markdown
	from django.utils.html import strip_tags
	def save(self, *args, **kwargs):
		if not self.excerpt:
			md = markdown.Markdown(extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
			])
			self.excerpt = strip_tags(md.convert(self.body))[:54]
		super(Post, self).save(*args, **kwargs)			

	def __str__(self):
		return self.title

	#自定义get_absolute_url方法,reverse方法用于返回指定函数参数的URL
	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})

	'''
	指定排序属性
	class Meta:
		ordering = ['-created_time']
	'''

