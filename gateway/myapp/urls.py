from django.urls import path
from .views import (
    auth_login_view, 
    auth_register_view, 
    create_blog_view, 
    get_blog_view, 
    test_view,
    )

urlpatterns = [
    path('auth/login', auth_login_view, name='login'),
    path('auth/register', auth_register_view, name='login'),
    path('blogs', create_blog_view, name='createBlog'),
    path('blogs/<str:blogUrl>', get_blog_view, name='getBlog'),
    path('test', test_view, name='test'),
]
