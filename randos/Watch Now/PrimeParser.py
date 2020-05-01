from bs4 import BeautifulSoup as bs
from difflib import SequenceMatcher
import operator


# create a class to understand the movie rows
class Movie:
    def __init__(self, row):
        mini_soup = bs(str(row), 'html.parser')

        self.link = mini_soup.find("a", {"class": "propper-link"})
        self.views = mini_soup.find_all('td')[3].split()[0]


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def find_most_similar(target, entries):
    val_dict = {}
    # find closest match to name
    for entry in entries:
        sim_rating = similar(target, entry)
        val_dict[entry] = sim_rating

    if len(val_dict) > 0:
        max_value = max(val_dict.items(), key=operator.itemgetter(1))[0]
    else:
        return 'No movies were found'

    return max_value
