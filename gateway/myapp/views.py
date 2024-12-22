import grpc
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from proto import user_service_pb2, user_service_pb2_grpc
from .handler import errorReturn, auth_register_post_handler
from django.http import JsonResponse

logger = logging.getLogger('myapp')

def test_view(request):
    return JsonResponse({"test": "here"})

def auth_login_view(request):
    logger.info(request.method + ' /api/auth/login', request.body)

    with grpc.insecure_channel('user-service:50051') as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        response = stub.Authentication(user_service_pb2.AuthRequest(email="satria",password="test"))
    print("gRPC Response:", response)
    return JsonResponse({"test": response.authToken})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def auth_register_view(request):
    logger.info('AuthRegister: ', request)

    if request.method == "POST":
        print("here2")

        return auth_register_post_handler(request)
