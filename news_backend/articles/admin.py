from django.contrib import admin
from models import Category, Tag, Article, ArticleView, ArticleReaction, EditTask

# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(ArticleView)
admin.site.register(ArticleReaction)
admin.site.register(EditTask)
