import grpc
import logging
from proto import blog_service_pb2
from .general_struct import BlogStruct
from myapp.repository.blog_repository import getBlogByTitle, createBlog, getBlogByUrl
from proto import user_service_pb2, user_service_pb2_grpc

logger = logging.getLogger('myapp')

def createBlogHandler(request) -> blog_service_pb2.CreateBlogResponse:
    newBlog = BlogStruct(request.writerId, request.title, request.content)

    if not newBlog.writerId:
        return blog_service_pb2.CreateBlogResponse(isSuccess=False, errorMsg= "User must be authenticated", url="")
    elif not newBlog.title:
        return blog_service_pb2.CreateBlogResponse(isSuccess=False, errorMsg= "Title must be provided", url="")
    elif not newBlog.content:
        return blog_service_pb2.CreateBlogResponse(isSuccess=False, errorMsg= "Content must be provided", url="")

    blog = getBlogByTitle(newBlog.title)

    if blog:
        return blog_service_pb2.CreateBlogResponse(isSuccess=False, errorMsg= "Blog by the same title already exist", url="")

    blog = createBlog(newBlog)

    return blog_service_pb2.CreateBlogResponse(isSuccess=True, errorMsg= "", url=blog.url)

def getBlogDetailHandler(request) -> blog_service_pb2.GetBlogDetailResponse:
    if not request.url:
        return getBlogDetailErrorResponse("please provide url")

    blog = getBlogByUrl(request.url)

    if not blog:
        return getBlogDetailErrorResponse("blog not found")

    with grpc.insecure_channel('user-service:50051') as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        writer = stub.GetUserById(user_service_pb2.GetUserByIdRequest(id=blog.writerId))

    if not writer.isSuccess:
        logger.error("GetUserByIdRequest: %s", writer.errorMsg)

    response = blog_service_pb2.GetBlogDetailResponse(
        isSuccess=True, 
        errorMsg= "", 
        blogTitle=blog.title,
        blogContent=blog.content,
        blogCreatedAt=str(blog.created_at),
        writerId=blog.writerId,
        writerName=writer.name,
        )
    
    return response

def getBlogDetailErrorResponse(errorMsg: str) -> blog_service_pb2.GetBlogDetailResponse:
    return blog_service_pb2.GetBlogDetailResponse(isSuccess=False, errorMsg= errorMsg)
