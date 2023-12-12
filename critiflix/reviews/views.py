from django.shortcuts import render, get_object_or_404
from .models import Movie, Review
from .utils import average_rating

def movie_list(request):
    movies = Movie.objects.all()
    movie_list = []

    for movie in movies:
        reviews = Review.objects.filter(movie=movie)

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
    movie=get_object_or_404(Movie, pk=pk)
    reviews=movie.reviews.all()
    
    if reviews:
        movie_rating = average_rating([review.rating for review in reviews])
        
        context = {'movie': movie, 'movie_rating': movie_rating, 'reviews': reviews}

    else:
        context = {'movie': movie, 'movie_rating': None, 'reviews': None}

    return render(request, 'movie_detail.html', context)

def base(request):
    return render(request, 'base.html')

