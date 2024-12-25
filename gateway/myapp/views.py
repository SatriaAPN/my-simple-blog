import logging
from .handler import (
    auth_register_post_handler, 
    auth_login_post_handler, 
    create_blog_post_handler,
    blog_detail_get_handler,
    blog_list_get_handler,
    token_refresh_post_handler,
    )
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

logger = logging.getLogger('myapp')

class BlogViewSet(ViewSet):
    # Permissions for each action
    permission_classes_by_action = {
        'list': [AllowAny],             # Public access
        'create': [IsAuthenticated],    # Requires authentication
        'retrieve': [AllowAny]
    }

    def get_permissions(self):
        try:
            # Return specific permissions for the action
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # Default permissions if not specified
            return [permission() for permission in self.permission_classes]

    # GET: List Blogs
    def list(self, request):
        logger.info(request.method + ' /api/blogs %s', request.GET)
        return blog_list_get_handler(request)

    # POST: Create Blog
    def create(self, request):
        logger.info(request.method + ' /api/blogs %s', str(request.body))
        return create_blog_post_handler(request)

    def retrieve(self, request, pk):
        logger.info(request.method + ' /api/blogs/' + pk)

        return blog_detail_get_handler(request, pk)

class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to hit the login endpoint
    
    def post(self, request):
        logger.info(request.method + ' /api/auth/login %s', request.body)

        return auth_login_post_handler(request)
    
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to hit the login endpoint
    
    def post(self, request):
        logger.info(request.method + ' /api/auth/register %s', request.body)

        return auth_register_post_handler(request)
    
class TokenRefreshView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to hit the login endpoint
    
    def post(self, request):
        logger.info(request.method + ' /api/token/refresh/ %s', request.body)

        return token_refresh_post_handler(request)