import json
import os
from reviews.models import Actor, Movie, MovieCasts, Review

def run():

    # Uzyskaj ścieżkę do katalogu, w którym znajduje się skrypt
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Uzyskaj ścieżkę do katalogu 'sourced_data'
    sourced_data_dir = os.path.join(script_dir, 'sourced_data')

    # Uzyskaj pełną ścieżkę do pliku movie_db.json
    file_path = os.path.join(sourced_data_dir, 'movie_db2.json')

    # Wczytaj dane z pliku movie_db.json
    with open(file_path, 'r') as movie_file:
        data = json.load(movie_file)

    # Dodaj filmy do bazy danych
    for movie_data in data.get("movies", []):
        movie = Movie.objects.create(
            movie_name=movie_data.get("movie_names"),
            publication_dates=movie_data.get("publication_dates"),
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
        movie_id=cast_data.get("movie_id")

        # Uzyskaj obiekt aktora, jeśli actor_id istnieje
        if actor_id:
            try:
                actor = Actor.objects.get(id=actor_id)
                movie = Movie.objects.get(id=movie_id)
                MovieCasts.objects.create(movie=movie, actor=actor, role=role)
            except Actor.DoesNotExist:
                print(f"Aktor o ID {actor_id} nie istnieje.")

        # Dodaj aktorów do bazy danych
    for review_data in data.get("reviews", []):
        Review.objects.create(
            username=review_data.get("username"),
            rating=review_data.get("rating"),
            content=review_data.get("content"),
            movie_id=review_data.get("movie_id"),
            dated_created=review_data.get("dated_created")
        )

if __name__ == "__main__":
    run()
