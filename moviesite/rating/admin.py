import xadmin
from .models import Mrating


class MratingAdmin():
    list_display = ['id', 'user', 'movie']
    
xadmin.site.register(Mrating, MratingAdmin)