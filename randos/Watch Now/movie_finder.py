from bs4 import BeautifulSoup as bs
import requests
from PrimeParser import find_most_similar, Movie

ROOT = 'https://www.primewire.li'

# get the movie that the user wants to watch
movie_str = 'the gentlemen'  # input("What movie would you like to watch?\n")
year = '2020'  # str(input("What year was it made?\n"))
movie_keywords = movie_str.split()

# format request
r = ""
for keyword in movie_keywords:
    r += f"{keyword}+"

# get from search page
primewire_request = requests.get(f"{ROOT}/?s={r}")

soup = bs(primewire_request.text, 'html.parser')

# get the most relevant movie title using string matching
titles_raw = soup.find_all('h2')
titles = {}

# clean titles to get the correct year
for title in titles_raw:
    string = title.text
    if (year in string.lower()):
        # get the href from the parent tag and assign it to the correct year
        parent = bs(str(title.parent), 'html.parser').find('a')
        href = parent['href']
        titles[string] = f"{ROOT}{href}"

# set a target and get the most similar
target = f"{movie_str} ({year})"
entries = list(titles.keys())

# get the most similar option
while True:
    most_similar = find_most_similar(target, entries)

    answer = input(f"Would you like to watch {most_similar}? (yes/no)\n")

    if 'yes' in answer.lower():
        break
    elif len(entries) == 1:
        print('All selections have been exhausted. Sorry.')
        break
    elif 'no' in answer.lower():
        entries.remove(most_similar)
    else:
        print('Please select yes or no...')

# get the link for the list of movies
movie_link = titles[most_similar]

# find the best link to watch on --> table = //div[@class="choose_tabs"]
database = requests.get(movie_link).text
link_soup = bs(database, 'html.parser')

table = link_soup.find("div", {"class": "choose_tabs"})

rows = table.find_all("table")

for row in rows:
    new_movie = Movie(row.find(""))
    print(f"link: {ROOT + new_movie.link}")
    print(f"views: {new_movie.views}")
