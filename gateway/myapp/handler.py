import grpc
import json
import logging
import jwt
from proto import (
  user_service_pb2_grpc,
  user_service_pb2,
  blog_service_pb2, 
  blog_service_pb2_grpc
  )
from django.http import JsonResponse
from datetime import datetime, timedelta
from myapp.general_struct import JwtDataStruct
from django.conf import settings

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

def create_blog_post_handler(request):
    userId = request.user.get("user_id")

    try:
      data = json.loads(request.body)
      title = data.get("title")
      content = data.get("content")
    except json.JSONDecodeError:
      return errorReturn("Invalid JSON", 400)

    with grpc.insecure_channel('blog-service:50051') as channel:
      stub = blog_service_pb2_grpc.BlogServiceStub(channel)
      response = stub.CreateBlog(blog_service_pb2.CreateBlogRequest(writerId=userId,title=title,content=content))

    if not response.isSuccess: 
      return errorReturn(response.errorMsg, 400)

    return JsonResponse(
      {
        "data": {
          "url": response.url,
        }
      }, 
      status=201
    )

def blog_detail_get_handler(request, blogUrl):
    with grpc.insecure_channel('blog-service:50051') as channel:
      stub = blog_service_pb2_grpc.BlogServiceStub(channel)
      response = stub.GetBlogDetail(blog_service_pb2.GetBlogDetailRequest(url=blogUrl))

    if not response.isSuccess: 
      return errorReturn(response.errorMsg, 400)

    return JsonResponse(
      {
        "data": {
          "type": "blogs",
          "attributes": {
            "title": response.blogTitle,
            "content": response.blogContent,
            "published_at": response.blogCreatedAt
          },
          "relationships": {
            "writer": {
              "data": {
                "type": "writers",
                "id": response.writerId,
                "name": response.writerName
              }
            }
          }
        },
      }
      ,
      status=200
    )

def blog_list_get_handler(request):
    page = int(request.GET.get('page', 1))
    pageSize = 10

    with grpc.insecure_channel('blog-service:50051') as channel:
      stub = blog_service_pb2_grpc.BlogServiceStub(channel)
      response = stub.GetBlogList(blog_service_pb2.GetBlogListRequest(page=page,pageSize=pageSize))

    if not response.isSuccess: 
      return errorReturn(response.errorMsg, 400)

    blogs = []

    for blog in response.blogs:
      blogs.append({
        "url":blog.url,
        "title":blog.title,
        "createdAt":blog.createdAt
      })

    return JsonResponse(
      {
        "meta": {
          "total": response.totalCount,
          "prevPage": response.prevPage,
          "currentPage":  response.page,
          "nextPage": response.nextPage,
          "blogPerPage": pageSize
        },
        "data": blogs
      }
      ,
      status=200
    )

def token_refresh_post_handler(request):
  try:
    # Parse the incoming JSON request
    body = json.loads(request.body)
    refresh_token = body.get("refresh_token")
    logger.info("here", refresh_token)
    # Decode the refresh token
    decoded_token = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
    
    # Check if the token is expired
    if decoded_token["exp"] < datetime.now().timestamp():
      return errorReturn("Refresh token is expired.", 401)
    
    # Ensure it is a refresh token
    if decoded_token["token_type"] != "refresh":
      return errorReturn("Invalid token type.", 401)

    access_exp = datetime.now() + timedelta(minutes=60)

    new_access_token = jwt.encode(
      {
        "user_id": decoded_token["user_id"],
        "user_role": decoded_token["user_role"],
        "exp": access_exp,
        "token_type": "access",
        "jti": decoded_token["jti"]  # Preserve the same jti
      },
      settings.SECRET_KEY,
      algorithm="HS256"
    )

    return JsonResponse(
      {
        "data": {
          "type": "token",
          "attributes": {
            "access_token": new_access_token,
            "token_type": "Bearer",
          },
        }
      }
    )

  except jwt.ExpiredSignatureError:
    return errorReturn("Refresh token has expired.", 401)
  except jwt.InvalidTokenError:
    return errorReturn("Invalid token.", 401)
  except Exception as e:
    return errorReturn(str(e), 401)

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