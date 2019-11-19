from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Movie, Recommendation
from rating.models import Mrating
from comment.models import Comment
from django.core.cache import cache
from kafka import KafkaProducer
from random import sample, uniform

import time

producer = KafkaProducer(bootstrap_servers='cloud3:9092,cloud4:9092,cloud5:9092')


def get_movies(genres_name): 
    movies_all = cache.get('movie_'+genres_name)
    if not movies_all:
        if genres_name == 'hot':
            movies_all = Movie.objects.all().order_by('-rating') 
        elif genres_name == 'new':
            movies_all = Movie.objects.all().order_by('-year') 
        else:
            movies_all = Movie.objects.filter(genres__name=genres_name)
        cache.set('movie_'+genres_name,movies_all,600)
    return movies_all
        
def page_movie(request, movies_all):
    paginator = Paginator(movies_all, 12)
    page_num = request.GET.get('page', 1)
    movies = paginator.get_page(page_num)
    page_num = movies.number
    page_range = range(max(1, page_num-5),min(page_num+6, paginator.num_pages+1))
    return render(request, 'movie_list.html', {'movies': movies, 'paginator':paginator})

def movie_recommendation_list(request):
    if request.user.is_authenticated:
        if request.user.recommendations.count() == 0:
            movies_all = sample(list(get_movies('hot')), 30)
            for movie in movies_all:
                recommendation = Recommendation.objects.create(movie=movie,weight=uniform(8, 12))
                request.user.recommendations.add(recommendation)
            request.user.save()
        recommendations_all = request.user.recommendations.all()[:12]
        movies_all = [each.movie for each in recommendations_all]
    else:
        movies_all = sample(list(get_movies('hot')), 12)
    return page_movie(request, movies_all)

def movie_hot_list(request):
    movies_all = get_movies('hot')
    return page_movie(request, movies_all)

def movie_new_list(request):
    movies_all = get_movies('new')
    return page_movie(request, movies_all)

def movie_action_list(request):
    movies_all = get_movies('Action')
    return page_movie(request, movies_all)

def movie_adventure_list(request):
    movies_all = get_movies('Adventure')
    return page_movie(request, movies_all)

def movie_science_list(request):
    movies_all = get_movies('Sci-Fi')
    return page_movie(request, movies_all)

def movie_thriller_list(request):
    movies_all = get_movies('Thriller')
    return page_movie(request, movies_all)

def movie_romance_list(request):
    movies_all = get_movies('Romance')
    return page_movie(request, movies_all)

def movie_amimation_list(request):
    movies_all = get_movies('Animation')
    return page_movie(request, movies_all)

def movie_children_list(request):
    movies_all = get_movies('Children')
    return page_movie(request, movies_all)

def movie_comedy_list(request):
    movies_all = get_movies('Comedy')
    return page_movie(request, movies_all)

def movie_documentary_list(request):
    movies_all = get_movies('Documentary')
    return page_movie(request, movies_all)

def movie_search(request):
    content = request.GET.get('content')
    movies_all = Movie.objects.filter(name__icontains=content)
    return page_movie(request, movies_all)
    
def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if request.method == "POST":
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        if content:
            comment = Comment.objects.create(user=request.user, movie=movie, content=content)
            comment.save()
        if rating:
            producer.send('django', (str(request.user.id)+' '+str(movie_id)+' '+str(rating)).encode('utf-8'))
            mrating = Mrating.objects.create(user=request.user, movie=movie, rating=rating)
            mrating.save()
        return redirect('/movie/'+str(movie_id))
    else:
        if request.user.is_authenticated:
            producer.send('django', (str(request.user.id)+' '+str(movie_id)+' 3.5').encode('utf-8'))
        try:
            rating = Mrating.objects.get(user=request.user, movie=movie)
        except:
            rating = None
        comments = Comment.objects.filter(movie=movie)
        return render(request, 'movie_detail.html', {'movie': movie, 'rating': rating, 'comments':comments})
