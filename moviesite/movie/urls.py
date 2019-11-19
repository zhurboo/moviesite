from django.urls import path, include
from movie.views import *

urlpatterns = [
    path('', movie_recommendation_list, name='recommendation'),
    path('hot', movie_hot_list, name='hot'),
    path('new', movie_new_list, name='new'),
    path('action', movie_action_list, name='action'),
    path('adventure', movie_adventure_list, name='adventure'),
    path('science', movie_science_list, name='science'),
    path('thriller', movie_thriller_list, name='thriller'),
    path('romance', movie_romance_list, name='romance'),
    path('amimation', movie_amimation_list, name='amimation'),
    path('children', movie_children_list, name='children'),
    path('comedy', movie_comedy_list, name='comedy'),
    path('documentary', movie_documentary_list, name='documentary'),
    path('search', movie_search, name='search'),
    path('movie/<int:movie_id>', movie_detail, name='detail'),
]