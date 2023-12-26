#importing libraries
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
# Function to get the HTML content of a page
def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')
# Function to scrape details of a single movie
# Pause for 2 seconds before making a request to avoid overloading the server
def scrape_movie_details(url):
    time.sleep(2)
    soup = get_soup(url)
    if not soup:
        return None

    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else "N/A"

    rating_element = soup.find("span", class_="sc-bde20123-1 cMEQkK")
    rating = rating_element.text.strip() if rating_element else "N/A"

    list_items = soup.find_all("li", role="presentation", class_="ipc-inline-list__item")
    length = next((item.text.strip() for item in list_items if "h" in item.text and "m" in item.text), "N/A")

    director_tag = soup.find("a", href=lambda href: href and "ref_=tt_ov_dr" in href)
    director = director_tag.text.strip() if director_tag else "N/A"

    metascore_tag = soup.find("span", class_="metacritic-score-box")
    metascore = metascore_tag.text.strip() if metascore_tag else "N/A"

    release_year_tag = soup.find("a", href=lambda href: href and "ref_=tt_ov_rdat" in href)
    release_year = release_year_tag.text.strip() if release_year_tag else "N/A"

    return {
        "title": title,
        "director": director,
        "metascore": metascore,
        "release_year": release_year,
        "rating": rating,
        "length": length
    }

# Function to scrape a list of movies from a given URL
def scrape_movie_list(url):
    soup = get_soup(url)
    movies = []

    for item in soup.find_all("a", class_="ipc-title-link-wrapper"):
        title_tag = item.find("h3", class_="ipc-title__text")
        if title_tag:
            title = title_tag.text
            link = "https://www.imdb.com" + item['href']
            movie_details = scrape_movie_details(link)
            movies.append((title, link, movie_details))

    return movies

# Scraping the movie list
movie_list_url = "https://www.imdb.com/chart/top/"
movies = scrape_movie_list(movie_list_url)
# Displaying the scraped data
for movie in movies:
    print(
        f"Rank: {movie[0]}, IMDB Rating: {movie[2]['rating']}, Director: {movie[2]['director']}, Metascore: {movie[2]['metascore']}, Release Year: {movie[2]['release_year']}, Duration: {movie[2]['length']}")
# Preparing data for DataFrame
imdb_data = []
for movie in movies:
    movie_data = {
        'Rank': movie[0],
        'IMDB Rating': movie[2]['rating'],
        'Director': movie[2]['director'],
        'Metascore': movie[2]['metascore'],
        'Release Year': movie[2]['release_year'],
        'Duration': movie[2]['length']
    }
    imdb_data.append(movie_data)

# Now, create the DataFrame
imdb_df = pd.DataFrame(imdb_data)
filename2 = "scraped_data.csv"
imdb_df.to_csv(filename2, index=False)
#duplicate rows to impure the dataset
duplicate_rows = imdb_df.sample(n=30, replace=True, random_state=1)
imdb_df = pd.concat([imdb_df, duplicate_rows], ignore_index=True)

np.random.seed(0)
num_negative = min(50, len(imdb_df))

# randomly select 50 rows to make it later negative
random_indices = np.random.choice(imdb_df.index, size=num_negative, replace=False)

#make those rows negative
imdb_df.loc[random_indices, 'IMDB Rating'] = imdb_df.loc[random_indices, 'IMDB Rating'] * -1
#save the scraped and impured data as a csv file
filename = "impured_data.csv"
imdb_df.to_csv(filename, index=False)

print(f"Data has been written to {filename}")

