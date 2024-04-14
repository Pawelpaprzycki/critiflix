
from django.urls import include, path
from . import views

urlpatterns = [
    
    path('movies/', views.movie_list, name = 'movie_list'),

   path('movies/<int:pk>', views.movie_detail, name = 'movie_detail'),

   path('', views.base, name = 'base'),

   path('movie_search/', views.movie_search, name='movie_search')
   ]

