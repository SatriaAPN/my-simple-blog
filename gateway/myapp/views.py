import grpc
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .handler import (
    auth_register_post_handler, 
    auth_login_post_handler, 
    create_blog_post_handler,
    blog_detail_get_handler,
    )
from django.http import JsonResponse

logger = logging.getLogger('myapp')

def test_view(request):
    return JsonResponse({"test": "here"})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def auth_login_view(request):
    logger.info(request.method + ' /api/auth/login %s', request.body)

    if request.method == "POST":
        return auth_login_post_handler(request)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def auth_register_view(request):
    logger.info(request.method + ' /api/auth/register %s', request.body)

    if request.method == "POST":
        return auth_register_post_handler(request)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def create_blog_view(request):
    logger.info(request.method + ' /api/blog %s', request.body)

    if request.method == "POST":
        return create_blog_post_handler(request)

@csrf_exempt
@api_view(['Get'])
@permission_classes([AllowAny])
def get_blog_view(request, blogUrl=None):
    logger.info(request.method + ' /api/blogs/' + blogUrl)

    if request.method == "GET":
        return blog_detail_get_handler(request, blogUrl)
