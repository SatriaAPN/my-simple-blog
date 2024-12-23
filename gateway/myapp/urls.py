from django.urls import path
from .views import auth_login_view, auth_register_view, create_blog_view, test_view  # Import the views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('auth/login', auth_login_view, name='login'),
    path('auth/register', auth_register_view, name='login'),
    path('blogs', create_blog_view, name='createBlog'),
    path('test', test_view, name='test'),
]
