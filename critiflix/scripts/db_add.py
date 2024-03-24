from datetime import datetime
import json
import os
from django.contrib.auth.models import User
from reviews.models import Actor, Movie, MovieCast, Review  

""" Aby uruchomić program należy znaleźć się w lokalizacji, gdzie znajduję się plik manage.py, 
    a następnie wpisać: 
    python manage.py runscript db_add """


def run():
    # Uzyskaj ścieżkę do katalogu, w którym znajduje się skrypt
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Uzyskaj ścieżkę do katalogu 'sourced_data'
    sourced_data_dir = os.path.join(script_dir, 'sourced_data')

    # Uzyskaj pełną ścieżkę do pliku movie_db.json
    file_path = os.path.join(sourced_data_dir, 'movie_db.json')

    # Wczytaj dane z pliku movie_db.json
    with open(file_path, 'r') as movie_file:
        data = json.load(movie_file)

    # Dodaj filmy do bazy danych
    for movie_data in data.get("movies", []):
        movie = Movie.objects.create(
            movie_name=movie_data.get("movie_names"),
            publication_dates=datetime.strptime(movie_data.get("publication_dates"), '%d.%m.%Y') if movie_data.get("publication_dates") else None,
            duration=movie_data.get("duration_field"),
            film_genre=movie_data.get("film_genre"),
            director=movie_data.get("directors")
        )

    # Dodaj aktorów do bazy danych
    for actor_data in data.get("actors", []):
        actor = Actor.objects.create(
            first_names=actor_data.get("first_names"),
            last_names=actor_data.get("last_names"),
            birth_dates=actor_data.get("birth_dates")
        )

    # Dodaj obsadę do bazy danych
    for cast_data in data.get("casts", []):
        actor_id = cast_data.get("actor_id")
        role = cast_data.get("role")
        movie_id = cast_data.get("movie_id")

        # Uzyskaj obiekt aktora, jeśli actor_id istnieje
        if actor_id:
            try:
                actor = Actor.objects.get(id=actor_id)
                movie = Movie.objects.get(id=movie_id)
                MovieCast.objects.create(movie=movie, actor=actor, role=role)
            except Actor.DoesNotExist:
                print(f"Aktor o ID {actor_id} nie istnieje.")

    for review_data in data.get("reviews", []):
        movie_id = review_data.get("movie_id")

        # Uzyskaj obiekt filmu, jeśli movie_id istnieje
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            print(f"Film o ID {movie_id} nie istnieje.")

        # Uzyskaj bieżącego użytkownika
        username = review_data.get("username")
        creator, created = User.objects.get_or_create(username=username)

        # Dodaj recenzję do bazy danych
        review, created = Review.objects.get_or_create(
            content=review_data.get("content"),
            rating=review_data.get("rating"),
            date_created=review_data.get("date_created"),
            date_edited=review_data.get("date_edited"),
            creator=creator,
            movie=movie
        )

if __name__ == "__main__":
    run()
