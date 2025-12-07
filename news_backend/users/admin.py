from django.contrib import admin
from models import User, Author, Editor, UserProfile, UserCustomization

# Register your models here.

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Editor)
admin.site.register(UserProfile)
admin.site.register(UserCustomization)
