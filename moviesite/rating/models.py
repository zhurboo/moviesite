from django.db import models
from user.models import User
from movie.models import Movie


class Mrating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(verbose_name='评分')
    
    class Meta:
        verbose_name = '评分'
        verbose_name_plural = verbose_name
        ordering = ['id']