import logging
from proto import blog_service_pb2
from .general_struct import BlogStruct
from myapp.repository.blog_repository import getBlogByTitle, createBlog

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
