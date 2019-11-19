from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='体裁名字')
    class Meta:
        verbose_name = '体裁'
        verbose_name_plural = verbose_name
        ordering = ['id']
    def __str__(self):
        return self.name

class Writer(models.Model):
    name = models.CharField(max_length=50, verbose_name='编剧名字')
    class Meta:
        verbose_name = '编剧'
        verbose_name_plural = verbose_name
        ordering = ['id']
    def __str__(self):
        return self.name
    
class Director(models.Model):
    name = models.CharField(max_length=50, verbose_name='导演名字')
    class Meta:
        verbose_name = '导演'
        verbose_name_plural = verbose_name
        ordering = ['id']
    def __str__(self):
        return self.name
    
class Actor(models.Model):
    name = models.CharField(max_length=50, verbose_name='演员名字')
    class Meta:
        verbose_name = '演员'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name
    
class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='语言')
    class Meta:
        verbose_name = '语言'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    IMDB_id = models.CharField(max_length=7, verbose_name='IMDB编号')
    name = models.CharField(max_length=100, verbose_name='电影名字')
    year = models.IntegerField(verbose_name='上映年份')
    genres = models.ManyToManyField(Genre, verbose_name='体裁')
    duration = models.CharField(max_length=20, verbose_name='时长')
    summary = models.TextField(verbose_name='简介')
    writers = models.ManyToManyField(Writer, verbose_name='编剧')
    directors = models.ManyToManyField(Director, verbose_name='导演')
    actors = models.ManyToManyField(Actor, verbose_name='演员')
    language = models.ManyToManyField(Language, verbose_name='语言')
    rating = models.FloatField(verbose_name='评分')
    
    class Meta:
        verbose_name = '电影'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

class Recommendation(models.Model):
    movie = models.ForeignKey(Movie, default=None, on_delete=models.CASCADE, verbose_name='电影')
    weight = models.FloatField(verbose_name='权重')
    class Meta:
        verbose_name = '推荐电影'
        verbose_name_plural = verbose_name
        ordering = ['-weight']
    def __str__(self):
        return self.movie.name
