from datetime import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView

from blogs_site.models import Post, Blogger


class MainView(TemplateView):
    template_name = 'blog.html'

    def get(self, request, *args, **kwargs):
        ctx = dict()

        if request.user.is_authenticated:
            ctx['posts'] = Post.objects.filter(blogger=request.user)

        ctx['blog_personal'] = True

        return render(request, MainView.template_name, ctx)


class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'login.html'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class BlogsView(TemplateView):
    template_name = 'blogs.html'

    def get(self, request, *args, **kwargs):
        ctx = dict()

        ctx['bloggers'] = Blogger.objects.exclude(id=request.user.id)
        return render(request, BlogsView.template_name, ctx)


class BlogView(FormView):
    template_name = 'blog.html'

    def get(self, request, *args, **kwargs):
        ctx = dict()

        ctx['posts'] = Post.objects.filter(blogger=kwargs['blogger_id'])

        if request.user.is_authenticated and \
                request.user.subscriptions is not None and \
                kwargs['blogger_id'] in request.user.subscriptions:
            ctx['is_sub'] = True
        else:
            ctx['is_sub'] = False

        return render(request, BlogView.template_name, ctx)

    def post(self, request, *args, **kwargs):
        if 'sub' in request.POST:
            if request.user.subscriptions is None:
                request.user.subscriptions = list()
            request.user.subscriptions.append(kwargs['blogger_id'])
            request.user.save()
        else:
            request.user.subscriptions.remove(kwargs['blogger_id'])
            request.user.save()
        return self.get(request, *args, **kwargs)


class SubscriptionView(TemplateView):
    template_name = 'blogs.html'

    def get(self, request, *args, **kwargs):
        ctx = dict()

        if not request.user.is_authenticated:
            raise Http404()

        ctx['bloggers'] = Blogger.objects.filter(id__in=request.user.subscriptions).\
            exclude(id=request.user.id)
        return render(request, BlogsView.template_name, ctx)


class PostsView(TemplateView):
    template_name = 'posts.html'

    def get(self, request, *args, **kwargs):
        ctx = dict()

        if not request.user.is_authenticated:
            raise Http404()

        ctx['posts'] = Post.objects.\
            filter(blogger__in=request.user.subscriptions).\
            order_by('-create_date')
        return render(request, PostsView.template_name, ctx)


class PostView(TemplateView):
    template_name = ''


class CreatePostView(CreateView):
    model = Post
    fields = ['headline', 'text']
    template_name = 'create_post.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, CreatePostView.template_name)
        raise Http404()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.blogger = self.request.user
        self.object.create_date = datetime.now()
        self.object.save()
        return super().form_valid(form)