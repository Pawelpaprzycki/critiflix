from datetime import datetime
from django.contrib.auth.models import User
from reviews.models import Movie, Review

# Replace 'user1' with the desired username
desired_username = 'user1'

# Check if the user already exists, create one if not
user, created = User.objects.get_or_create(username=desired_username)

# If the user is newly created, set a password
if created:
    user.set_password('your_password')  # Replace 'your_password' with the desired password
    user.save()

# Replace 'Ojciec chrzestny' with the actual name of the movie you want to review
movie = Movie.objects.get(movie_name='Ojciec chrzestny')

# Replace 'your_content' with the actual content of the review
review_content = "An absolute masterpiece, one of the greatest films of all time."

# Replace 'your_rating' with the actual rating for the movie
review_rating = 5

# Replace 'your_date_created' with the actual date and time the review was created
review_date_created = datetime.now()

# Create a new review instance
new_review = Review.objects.create(
    content=review_content,
    rating=review_rating,
    date_created=review_date_created,
    creator=user,
    movie=movie
)

# Print the review ID to verify it was added successfully
print(f"Review ID: {new_review.id}")
