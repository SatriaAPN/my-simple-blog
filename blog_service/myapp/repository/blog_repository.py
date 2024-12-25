import logging
from myapp.models import Blog
from myapp.general_struct import BlogStruct
from django.core.paginator import Paginator

logger = logging.getLogger("myapp")


def getBlogByTitle(title: str) -> Blog:
  blog = Blog.objects.filter(title=title).first()

  return blog


def getBlogByUrl(url: str) -> Blog:
  blog = Blog.objects.filter(url=url).first()

  return blog


def getBlogList(page: int, pageSize: int) -> dict:
  blogs = Blog.objects.all()

  blogs = blogs.order_by("-created_at")

  # Pagination
  paginator = Paginator(blogs, pageSize)
  paginatedBlogs = paginator.get_page(page)

  response = {
      "blogs": [],
      "totalCount": paginator.count,
  }

  for blog in paginatedBlogs:
    response["blogs"].append(
        {
            "url": blog.url,
            "title": blog.title,
            "createdAt": blog.created_at,
            "writerId": blog.writerId,
        }
    )

  return response


def createBlog(blogData: BlogStruct) -> Blog:
  url = generateUrl(blogData.title)

  blog = Blog.objects.create(
      writerId=blogData.writerId,
      title=blogData.title,
      content=blogData.content,
      url=url,
  )

  return blog


def generateUrl(title: str) -> str:
  url = title.split(" ")
  return "-".join(url)
