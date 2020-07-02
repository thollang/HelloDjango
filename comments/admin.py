from django.contrib import admin
from comments.models import Comment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'url', 'post', 'created_time']
    fields = ['name', 'email', 'url', 'text', 'post']

admin.site.register(Comment, CommentAdmin)