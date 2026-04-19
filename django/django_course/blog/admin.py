from django.contrib import admin
from .models import News, Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_published', 'created_at']
    list_filter = ['date_published', 'author']
    search_fields = ['title', 'content']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['news', 'user', 'date_created', 'is_active']
    list_filter = ['is_active', 'date_created']