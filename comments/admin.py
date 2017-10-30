from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
	list_display = ['name','created_time','url','post']

admin.site.register(Comment,CommentAdmin)
