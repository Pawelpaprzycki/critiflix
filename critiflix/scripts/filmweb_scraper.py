import requests
import json
import os
from bs4 import BeautifulSoup

output_file_path = os.path.join('sourced_data', 'movie_db.json')

url_base = 'https://www.filmweb.pl/ranking/vod/netflix/film/'
start_year = 1970
end_year = 2024

data = {"movies": [], "actors": [], "casts": [], "reviews": []}
movie_id_counter = 1
actor_id_counter = 1

def get_actor_id(actor_name):
    for actor in data["actors"]:
        if actor["first_names"] + " " + actor["last_names"] == actor_name:
            return actor["id"]
    return None

def parse_publication_date(publication_date_str, year):
    if publication_date_str.strip():  # Check if the publication date string is not empty
        parts = publication_date_str.split()  # Split the string by spaces
        
        if parts[0].isdigit() and (len(parts[0]) == 2 or len(parts[0]) == 1):  # Check if it contains day, month, and year
            day = int(parts[0])
            month_str = parts[1].lower()
            months = {
                'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4, 'maja': 5, 'czerwca': 6,
                'lipca': 7, 'sierpnia': 8, 'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12
            }
            month = months.get(month_str)
            if month is None:
                return f"01.01.{year}"
            return f"{day:02d}.{month:02d}.{year}"
        else:
            day = 1
            month = 1
            
            return f"01.01.{year}"
    else:
        return f"01.01.{year}"


for year in range(start_year, end_year + 1):
    url_movies = f'{url_base}{year}'

    movie_response = requests.get(url_movies)
    movie_soup = BeautifulSoup(movie_response.text, 'html.parser')
    movie_elements = movie_soup.find_all('h2', class_='rankingType__title')

    for element in movie_elements:
        movie_title = element.get_text()
        movie_link = element.find('a', itemprop='url')
        full_movie_link = f"https://www.filmweb.pl{movie_link['href']}"
        print(full_movie_link)

        movie_response2 = requests.get(full_movie_link)
        movie_soup2 = BeautifulSoup(movie_response2.text, 'html.parser')

        director_span = movie_soup2.find('span', itemprop='name')
        if director_span:
            director = director_span.get_text()
        else:
            director = movie_soup2.find('h1', class_='filmCoverSection__title').get_text()

        film_genre = movie_soup2.find('div', class_='filmInfo__info', itemprop='genre').get_text()
        publication_date_span = movie_soup2.find('span', itemprop='datePublished')
        if publication_date_span:
            publication_date = publication_date_span.get_text()
            # Parse publication date
            publication_date = parse_publication_date(publication_date, year)
        else:
            publication_date = f"01.01.{year}"  # Default date if publication date not found

        # Sprawdzenie, czy istnieje element z czasem trwania przed próbą pobrania tekstu
        time_required_elem = movie_soup2.find('div', itemprop='timeRequired')
        if time_required_elem:
            time_required = time_required_elem.get_text()
        else:
            time_required = None

        actors = movie_soup2.find_all('h3', itemprop='name')
        roles = movie_soup2.find_all('span', itemprop='alternateName')

        cast = []
        for actor, role in zip(actors, roles):
            actor_name = actor.get_text()
            role_name = role.get_text()

            actor_name_parts = actor_name.split()
            if len(actor_name_parts) < 2:
                continue

            actor_id = get_actor_id(actor_name)
            if actor_id is None:
                actor_id = actor_id_counter
                actor_id_counter += 1
                actor_info = {
                    "id": actor_id,
                    "first_names": actor_name_parts[0],
                    "last_names": actor_name_parts[1],
                    "birth_dates": ""
                }
                data["actors"].append(actor_info)

            cast_item = {
                "actor_id": actor_id,
                "movie_id": movie_id_counter,
                "role": role_name
            }
            cast.append(cast_item)

        movie_info = {
            "id": movie_id_counter,
            "movie_names": movie_title,
            "publication_dates": publication_date,
            "duration_field": time_required,
            "film_genre": film_genre,
            "directors": director
        }
        reviews = []
        full_movie_link2 = f"https://www.filmweb.pl{movie_link['href']}/reviews"
        

        movie_response3 = requests.get(full_movie_link2)
        movie_soup3 = BeautifulSoup(movie_response3.text, 'html.parser')

        usernames = movie_soup3.find_all('a', class_='flatReview__name')
        ratings = movie_soup3.find_all('div', class_='flatReview__rate')
        contents = movie_soup3.find_all('div', class_='flatReview__text')  

        for username, rating, content in zip(usernames, ratings, contents):
            username1 = username.get_text()
            username2 = username1[1:len(username1)-1]
            rating1 = rating.get_text()
            content1 = content.get_text()
            
            review_item = {
                "username": username2,
                "rating": rating1,
                "content": content1,
                "movie_id": movie_id_counter,
            }
            reviews.append(review_item)
        
        data["movies"].append(movie_info)
        data["casts"].extend(cast)
        data["reviews"].extend(reviews)
        movie_id_counter += 1

# Save data to the output file
with open(output_file_path, "w") as f:
    json.dump(data, f, indent=2)
