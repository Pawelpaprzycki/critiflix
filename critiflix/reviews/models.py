from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Actor(models.Model):
    first_names = models.CharField(max_length=50, help_text="First name")
    last_names = models.CharField(max_length=50, help_text="Last name")
    birth_dates = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.first_names


class Movie(models.Model):
    movie_name = models.CharField(max_length=50)
    publication_dates = models.DateField(help_text="Publication date of the movie/series", null=True, blank=True)
    duration = models.CharField(max_length=50, default='99', null=True, blank=True)
    film_genre = models.CharField(max_length=50)
    director = models.CharField(max_length=50)
    website = models.URLField(default="http://www.netflix.com/pl/")

    def __str__(self):
        return f"{self.movie_name} - {self.director}"

class MovieCast(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, help_text="Name of the role")

    def __str__(self):
        return f"{self.actor} as {self.role} in {self.movie}"

class Review(models.Model):
    content = models.TextField(help_text="Review of the movie/series.")
    rating = models.PositiveIntegerField(default=0, help_text="Rating of the movie/series from 1 to 10.", 
                                         validators=[MaxValueValidator(10),MinValueValidator(1)])
    date_created = models.DateTimeField(auto_now_add=True, help_text="Date of writing the review.")
    date_edited = models.DateTimeField(null=True, help_text="Date and time of the last review edit.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews', help_text="Reviewed Movie/series.")
    

    def __str__(self):
        return self.creator.username

