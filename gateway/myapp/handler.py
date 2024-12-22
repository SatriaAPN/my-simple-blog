import grpc
import json
import logging
from proto import user_service_pb2, user_service_pb2_grpc
from django.http import JsonResponse

logger = logging.getLogger('myapp')

def auth_register_view(request):
    if request.method == "POST":
        return auth_register_post_handler(request)

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