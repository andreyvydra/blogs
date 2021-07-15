from django.contrib import admin

# Register your models here.
from blogs_site.models import Blogger, Post


admin.site.register(Blogger)
admin.site.register(Post)
