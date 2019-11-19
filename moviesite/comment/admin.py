import xadmin
from .models import Comment


class CommentAdmin():
    list_display = ['id', 'user', 'movie']
    
xadmin.site.register(Comment, CommentAdmin)