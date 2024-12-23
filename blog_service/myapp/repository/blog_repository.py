import logging
from myapp.models import Blog
from myapp.general_struct import BlogStruct

logger = logging.getLogger('myapp')

def getBlogByTitle(title: str) -> Blog:
  blog = Blog.objects.filter(title=title).first()

  return blog

def createBlog(blogData: BlogStruct) -> Blog:
  url = generateUrl(blogData.title)

  blog = Blog.objects.create(
      writerId=blogData.writerId,
      title=blogData.title,
      content=blogData.content,
      url=url
  )

  return blog

def generateUrl(title: str) -> str:
  url = title.split(" ")
  return "-".join(url)