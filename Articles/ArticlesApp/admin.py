from django.contrib import admin
from .models import *
# Register your models here.

from .models import Article, Comment, Category, Bookmark


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'content', 'summary', 'created_at', 'reference', 'likes', 'publisher', 'category')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'article', 'created_at', 'user')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('article', 'user')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
