from django.contrib import admin
from reviews.models import Movie, MovieCast, Review, Actor

    
class MovieAdmin(admin.ModelAdmin):
    list_display=('movie_name', 'director')
    list_filter = ('director',)

class ActorAdmin(admin.ModelAdmin):
    list_display=('first_names', 'last_names')
    list_filter = ('last_names',)
    search_fields = ('last_names__startswith', 'first_names')


class MovieCastAdmin(admin.ModelAdmin):
    list_display=('actor_first_name',  'actor_last_name', 'role', 'movie',)
    list_filter = ('movie',)

    def actor_first_name(self, obj):
        return obj.actor.first_names
    
    def actor_last_name(self, obj):
        return obj.actor.last_names
    
class ReviewAdmin(admin.ModelAdmin):
    list_display=('movie','rating','creator','content',)
    list_filter = ('movie',)

admin.site.register(MovieCast, MovieCastAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Movie, MovieAdmin)