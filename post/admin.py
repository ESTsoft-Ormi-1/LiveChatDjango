from django.contrib import admin

from post.models import Post, Tag, Category


# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)

