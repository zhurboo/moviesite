from django.db import models
from user.models import User
from movie.models import Movie


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='评论内容')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['id']