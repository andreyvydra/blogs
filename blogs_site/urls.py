from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainView.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.Logout.as_view()),
    path('posts', views.PostsView.as_view()),
    path('post/<int:post_id>', views.PostView.as_view()),
    path('change_post/<int:post_id>', views.UpdatePostView.as_view()),
    path('create_post', views.CreatePostView.as_view()),
    path('blogs', views.BlogsView.as_view()),
    path('blog/<int:blogger_id>', views.BlogView.as_view()),
    path('subscriptions', views.SubscriptionView.as_view())
]
