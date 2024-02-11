from django.contrib.admin import AdminSite

from reviews.models import Movie, MovieCasts, Review, Actor


class CritiflixAdminSite(AdminSite):
    title_header = 'Aplikacja administracyjna Critiflix'
    site_header = 'Aplikacja administracyjna Critiflix'
    index_title = 'Administracja witryną Critiflix'


movie_admin_site = CritiflixAdminSite(name='critiflix')

movie_admin_site.register(Movie)
movie_admin_site.register(MovieCasts)
movie_admin_site.register(Review)
movie_admin_site.register(Actor)