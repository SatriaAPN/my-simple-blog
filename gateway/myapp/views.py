import grpc
from proto import user_service_pb2, user_service_pb2_grpc

from django.http import JsonResponse

def test_view(request):
    return JsonResponse({"test": "here"})

def auth_login_view(request):
    with grpc.insecure_channel('user-service:50051') as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        response = stub.Authentication(user_service_pb2.AuthRequest(email="satria",password="test"))
    print("gRPC Response:", response)
    return JsonResponse({"test": response.authToken})

def auth_register_view(request):
    return JsonResponse({"test": "here"})
