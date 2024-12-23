import grpc
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .handler import auth_register_post_handler, auth_login_post_handler, create_blog_post_handler
from django.http import JsonResponse

logger = logging.getLogger('myapp')

def test_view(request):
    return JsonResponse({"test": "here"})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def auth_login_view(request):
    logger.info(request.method + ' /api/auth/login', request.body)

    if request.method == "POST":
        return auth_login_post_handler(request)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def auth_register_view(request):
    logger.info(request.method + ' /api/auth/register', request.body)

    if request.method == "POST":
        return auth_register_post_handler(request)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def create_blog_view(request):
    logger.info(request.method + ' /api/blog', request.body)

    if request.method == "POST":
        return create_blog_post_handler(request)
