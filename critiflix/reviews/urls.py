from reviews.admin import movie_admin_site
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', movie_admin_site.urls),

    path('movies/', views.movie_list, name = 'movie_list'),

   path('movies/<int:pk>', views.movie_detail, name = 'movie_detail'),

   path('', views.base, name = 'base')
   ]

