from django.contrib import admin
from models import Reaction, PostReaction, CommentReaction, Post, Comment, PostImage

# Register your models here.

admin.site.register(Reaction)
admin.site.register(Post)
admin.site.register(PostReaction)
admin.site.register(PostImage)
admin.site.register(Comment)
admin.site.register(CommentReaction)
