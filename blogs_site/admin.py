from django.contrib import admin

# Register your models here.
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from blogs.settings import DEFAULT_FROM_EMAIL
from blogs_site.models import Blogger, Post
from blogs_site.views import send_message


class PostAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super(PostAdmin, self).save_model(request, obj, form, change)
        bloggers = Blogger.objects.all()
        subs = [i for i in bloggers if obj.blogger.id in i.subscriptions]
        emails = [sub.email for sub in subs]
        send_message(emails, obj.blogger, obj.headline)


class BloggerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super(BloggerAdmin, self).save_model(request, obj, form, change)
        obj.password = make_password(obj.password)
        obj.save()


admin.site.register(Blogger, BloggerAdmin)
admin.site.register(Post, PostAdmin)
