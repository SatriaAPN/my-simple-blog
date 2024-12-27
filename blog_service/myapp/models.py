from django.db import models


class Blog(models.Model):
  writerId = models.IntegerField(blank=False)
  title = models.CharField(max_length=300)
  content = models.CharField(max_length=12000)
  url = models.CharField(max_length=200)
  isHiden = models.BooleanField(default=False)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.title
