import grpc
import json
import logging
import jwt
from http import HTTPStatus
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
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger('myapp')


def auth_register_post_handler(request):
  try:
    data = json.loads(request.body)
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
  except json.JSONDecodeError:
    return errorReturn("Invalid JSON", HTTPStatus.BAD_REQUEST)

  with grpc.insecure_channel('user-service:50051') as channel:
    stub = user_service_pb2_grpc.UserServiceStub(channel)

    response = stub.CreateUser(user_service_pb2.CreateUserRequest(
        name=name, email=email, password=password))

  if not response.isSuccess:
    return errorReturn(response.errorMsg, HTTPStatus.BAD_REQUEST)

  return JsonResponse(
      {
          "data": {
              "id": response.userId,
          }
      },
      status=HTTPStatus.CREATED
  )

def auth_login_post_handler(request):
  try:
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")
  except json.JSONDecodeError:
    return errorReturn("Invalid JSON", HTTPStatus.BAD_REQUEST)

  with grpc.insecure_channel('user-service:50051') as channel:
    stub = user_service_pb2_grpc.UserServiceStub(channel)
    response = stub.Authentication(
        user_service_pb2.AuthRequest(email=email, password=password))

  if not response.isSuccess:
    return errorReturn(response.errorMsg, HTTPStatus.BAD_REQUEST)

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
      },
      status=HTTPStatus.OK
  )

def create_blog_post_handler(request):
  userId = request.user.get("user_id")

  try:
    data = json.loads(request.body)
    title = data.get("title")
    content = data.get("content")
  except json.JSONDecodeError:
    return errorReturn("Invalid JSON", HTTPStatus.BAD_REQUEST)

  with grpc.insecure_channel('blog-service:50051') as channel:
    stub = blog_service_pb2_grpc.BlogServiceStub(channel)
    response = stub.CreateBlog(blog_service_pb2.CreateBlogRequest(
        writerId=userId, title=title, content=content))

  if not response.isSuccess:
    return errorReturn(response.errorMsg, HTTPStatus.BAD_REQUEST)

  return JsonResponse(
      {
          "data": {
              "url": response.url,
          }
      },
      status=HTTPStatus.CREATED
  )

def update_blog_hide_handler(request):
  if request.user.get("user_role") != "admin":
    return errorReturn("Unauthorized", HTTPStatus.UNAUTHORIZED)

  try:
    data = json.loads(request.body)
    url = data.get("url")
    hide = data.get("hide")
  except json.JSONDecodeError:
    return errorReturn("Invalid JSON", HTTPStatus.BAD_REQUEST)
  
  if not url:
    return errorReturn("url variable is missing", HTTPStatus.BAD_REQUEST)
  if hide == None:
    return errorReturn("hide variable is missiing", HTTPStatus.BAD_REQUEST)

  with grpc.insecure_channel('blog-service:50051') as channel:
    stub = blog_service_pb2_grpc.BlogServiceStub(channel)
    response = stub.UpdateBlogHideInfo(blog_service_pb2.UpdateBlogHideInfoRequest(
        url=url,hide=hide))
    logger.info("here %s", response)
  if not response.isSuccess:
    return errorReturn(response.errorMsg, HTTPStatus.BAD_REQUEST)

  return JsonResponse(
      {
          "data": {
              "url": url,
              "hide": hide
          }
      },
      status=HTTPStatus.OK
  )

def blog_detail_get_handler(request, blogUrl):
  with grpc.insecure_channel('blog-service:50051') as channel:
    stub = blog_service_pb2_grpc.BlogServiceStub(channel)
    response = stub.GetBlogDetail(
        blog_service_pb2.GetBlogDetailRequest(url=blogUrl))

  if not response.isSuccess:
    return errorReturn(response.errorMsg, HTTPStatus.BAD_REQUEST)

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
      },
      status=HTTPStatus.OK
  )

def blog_list_get_handler(request):
  page = int(request.GET.get('page', 1))
  pageView  = request.GET.get('pageView', 'home')
  pageSize = 10
  showHiden = False
  logger.info(request.user)
  logger.info(type(request.user))

  if request.user.is_authenticated and request.user.get("user_role") == "admin":
    showHiden = pageView == 'admin-management'

  with grpc.insecure_channel('blog-service:50051') as channel:
    stub = blog_service_pb2_grpc.BlogServiceStub(channel)
    response = stub.GetBlogList(
        blog_service_pb2.GetBlogListRequest(page=page, pageSize=pageSize, showHiden=showHiden))

  if not response.isSuccess:
    return errorReturn(response.errorMsg, HTTPStatus.BAD_REQUEST)

  blogs = []

  for blog in response.blogs:
    newBlog = {
        "url": blog.url,
        "title": blog.title,
        "createdAt": blog.createdAt
    }

    if showHiden:
      newBlog["isHiden"] = blog.isHiden

    blogs.append(newBlog)

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
      },
      status=HTTPStatus.OK
  )

def token_refresh_post_handler(request):
  try:
    body = json.loads(request.body)
    refresh_token = body.get("refresh_token")

    decoded_token = jwt.decode(
        refresh_token, settings.SECRET_KEY, algorithms=["HS256"])

    if decoded_token["exp"] < datetime.now().timestamp():
      return errorReturn("Refresh token is expired.", HTTPStatus.UNAUTHORIZED)

    if decoded_token["token_type"] != "refresh":
      return errorReturn("Invalid token type.", HTTPStatus.UNAUTHORIZED)

    access_exp = datetime.now() + timedelta(minutes=60)

    new_access_token = jwt.encode(
        {
            "user_id": decoded_token["user_id"],
            "user_role": decoded_token["user_role"],
            "exp": access_exp,
            "token_type": "access",
            "jti": decoded_token["jti"]
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
        },
        status=HTTPStatus.OK
    )

  except jwt.ExpiredSignatureError:
    return errorReturn("Refresh token has expired.", HTTPStatus.UNAUTHORIZED)
  except jwt.InvalidTokenError:
    return errorReturn("Invalid token.", HTTPStatus.UNAUTHORIZED)
  except Exception as e:
    return errorReturn(str(e), HTTPStatus.UNAUTHORIZED)

def errorReturn(msg: str, status: HTTPStatus) -> JsonResponse:
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
