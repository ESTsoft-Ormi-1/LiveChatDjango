from django.contrib import admin
from post.models import Post
from post.models import Tag


# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)