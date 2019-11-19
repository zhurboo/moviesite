import xadmin
from .models import Genre, Writer, Director, Actor, Language, Movie, Recommendation


class GenreAdmin():
    list_display = ['id', 'name']

class WriterAdmin():
    list_display = ['id', 'name']
    
class DirectorAdmin():
    list_display = ['id', 'name']
    
class ActorAdmin():
    list_display = ['id', 'name']

class LanguageAdmin():
    list_display = ['id', 'name']
    
class MovieAdmin():
    list_display = ['id', 'IMDB_id', 'name']
    
class RecommendationAdmin():
    list_display = ['id', 'movie', 'weight']
    
xadmin.site.register(Genre, GenreAdmin)
xadmin.site.register(Writer, WriterAdmin)
xadmin.site.register(Director, DirectorAdmin)
xadmin.site.register(Actor, ActorAdmin)
xadmin.site.register(Language, LanguageAdmin)
xadmin.site.register(Movie, MovieAdmin)
xadmin.site.register(Recommendation, RecommendationAdmin)