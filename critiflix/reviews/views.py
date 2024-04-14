from django.shortcuts import render
from .models import Movie, Actor
from .forms import SearchForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .utils import average_rating


def index(request):
    return render(request, "base.html")

def movie_search(request):
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    movies = set()

    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "movie_name"

        if search_in == "movie_name":
            movies = Movie.objects.filter(movie_name__icontains=search)
        else:
            # Szukanie filmów na podstawie aktora
            actor_movies = Movie.objects.filter(
                Q(moviecast__actor__first_names__icontains=search) |
                Q(moviecast__actor__last_names__icontains=search)
            ).distinct()

            movies = actor_movies.prefetch_related('moviecast_set__actor')

    return render(request, "search_results.html", {"form": form, "search_text": search_text, "movies": movies})

def movie_list(request):
    movies = Movie.objects.all()
    movie_list = []

    for movie in movies:
        reviews = movie.reviews.all()

        if reviews:
            movie_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            movie_rating = None
            number_of_reviews = 0

        movie_list.append({'movie': movie, 'movie_rating': movie_rating, 'number_of_reviews': number_of_reviews})

    context = {'movie_list': movie_list}
    return render(request, 'movie_list.html', context)

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = movie.reviews.all()

    if reviews:
        movie_rating = average_rating([review.rating for review in reviews])
        context = {'movie': movie, 'movie_rating': movie_rating, 'reviews': reviews}
    else:
        context = {'movie': movie, 'movie_rating': None, 'reviews': None}

    return render(request, 'movie_detail.html', context)

def base(request):
    return render(request, 'base.html')
