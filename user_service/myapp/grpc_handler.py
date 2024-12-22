from proto import user_service_pb2
from .general_struct import UserStruct
from myapp.repository.user_repository import getUserByEmail, createUser


def createUserHandler(request) -> user_service_pb2.CreateUserResponse:
  if not request.email:
      return user_service_pb2.CreateUserResponse(isSuccess=False, userId=0, errorMsg= "Email must not be empty")
  elif "@" not in request.email:
      return user_service_pb2.CreateUserResponse(isSuccess=False, userId=0, errorMsg= "Invalid email format")
  elif not request.password:
      return user_service_pb2.CreateUserResponse(isSuccess=False, userId=0, errorMsg= "Password must not be empty")
  elif len(request.password) < 6:
      return user_service_pb2.CreateUserResponse(isSuccess=False, userId=0, errorMsg= "Password must be at least 6 characters")
  elif not request.name:
      return user_service_pb2.CreateUserResponse(isSuccess=False, userId=0, errorMsg= "Name must not be empty")

  user = getUserByEmail(request.email)

  if user:
      return user_service_pb2.CreateUserResponse(isSuccess=False, userId=0, errorMsg= "email already registered")

  userData = UserStruct(name=request.name, email=request.email, password=request.password, role="admin")

  user = createUser(userData)

  return user_service_pb2.CreateUserResponse(isSuccess=True, userId=user.id, errorMsg= "")
