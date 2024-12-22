import grpc
import json
import logging
from proto import user_service_pb2, user_service_pb2_grpc
from django.http import JsonResponse

logger = logging.getLogger('myapp')

def auth_register_post_handler(request):
    try:
      data = json.loads(request.body)
      name = data.get("name")
      email = data.get("email")
      password = data.get("password")
    except json.JSONDecodeError:
      return errorReturn("Invalid JSON", 400)

    with grpc.insecure_channel('user-service:50051') as channel:
      stub = user_service_pb2_grpc.UserServiceStub(channel)
      response = stub.CreateUser(user_service_pb2.CreateUserRequest(name=name, email=email, password=password))
    logger.info("ini dia", response)

    if not response.isSuccess: 
      return errorReturn(response.errorMsg, 400)

    return JsonResponse(
      {
        "data": {
          "id": response.userId,
        }
      }, 
      status=201
    )

def auth_login_post_handler(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
    except json.JSONDecodeError:
        return errorReturn("Invalid JSON", 400)
    
    with grpc.insecure_channel('user-service:50051') as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        response = stub.Authentication(user_service_pb2.AuthRequest(email=email,password=password))

    if not response.isSuccess:
       return errorReturn(response.errorMsg, 403)
       
    return JsonResponse(
        {
            "data": {
                "type": "token",
                "attributes": {
                    "access_token": response.accessToken,
                    "refresh_token": response.refreshToken,
                    "token_type": "Bearer",
                },
            }
        }
    )
   

def errorReturn(msg: str, status: int) -> JsonResponse:
    return JsonResponse(
      {
        "errors": [
          {
          "status": status,
          "detail": msg,
          }
        ]
      },
      status=status
    )