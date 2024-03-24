from django.contrib import admin
from reviews.models import Movie, MovieCast, Review, Actor

    
class MovieAdmin(admin.ModelAdmin):
    list_display=('movie_name', 'director', 'publication_dates')
    list_filter = ('director',)
    date_hierarchy = 'publication_dates'
    search_fields = ('movie_name', 'director', )
   




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
    list_display=('creator','rating','content','movie')
    list_filter = ('movie',)
    
    fieldsets = ((None,{'fields':('creator','movie')}),('Zawartość recenzji',{'fields':('content', 'rating')}))

admin.site.register(MovieCast, MovieCastAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Movie, MovieAdmin)