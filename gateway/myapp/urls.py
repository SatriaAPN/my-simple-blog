from rest_framework.routers import DefaultRouter
from .views import (
    BlogViewSet,
    LoginView,
    RegisterView,
    TokenRefreshView,
    UpdateBlogHideView,
)
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

router = DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blogs')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/admin/blogs/hide/', UpdateBlogHideView.as_view(), name='blogs_hide'),
]
