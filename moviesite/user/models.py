from django.db import models
from django.contrib.auth.models import AbstractUser
from movie.models import Movie, Genre, Recommendation

class User(AbstractUser):
    age = models.IntegerField(verbose_name='年龄', default=0)
    sex = models.BooleanField(choices=((0,'男'),(1,'女'),), default=0, verbose_name='性别')
    interests = models.ManyToManyField(Genre, verbose_name='感兴趣')
    recommendations = models.ManyToManyField(Recommendation, verbose_name='推荐电影')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username
