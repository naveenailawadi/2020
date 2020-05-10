from bs4 import BeautifulSoup as bs
import requests
from jinja2 import Template
from datetime import datetime as dt
import random
import os

WEBSITES = ['https://www.washingtonpost.com', 'https://www.nytimes.com', 'https://www.economist.com']
MAX_PROCESSES = os.cpu_count() * 2

# create a class that handles html and turns them into documents


class Article:
    def __init__(self, raw_html, source):
        self.source = source

        # turn the html into a soup object
        soup = bs(raw_html, 'html.parser')

        # get the source and headline
        self.title = soup.find('h1').text

        # figure out the type of tags that the document carries for paragraphs
        # do this by comparing the length of them
        p_tags = soup.find_all('p')

        self.paragraphs = [tag.text for tag in p_tags]


# create a class that exports the documents
class Exporter:
    # create an init to add some necessary files
    def __init__(self):
        self.css = open('layout.css', 'r').read()
        self.template = Template(open('layout.html', 'r').read())

    def create_folder(self):
        today = dt.now()
        self.folder = f"News {today.month}-{today.day}-{today.year}"

        try:
            os.mkdir(self.folder)
        except FileExistsError:
            pass

        # enter the folder
        os.chdir(self.folder)

        # add the necessary documents
        with open('main.css', 'w') as outfile:
            outfile.write(self.css)

    def add_article(self, article):
        # handle if there is no folder
        if not self.folder:
            print('Folder must be added before adding a document!')
            return

        # add the document as html
        filename = f"{article.title.replace('/', ' - ')} - ({article.source}).html"
        with open(filename, 'w') as outfile:
            html_doc = self.template.render(title=article.title, source=article.source, paragraphs=article.paragraphs)

            # write it all to the outfile
            outfile.write(html_doc)


class Scraper:
    def print_grab_notifier(self, homepage):
        print('Grabbing headlines from ' + homepage + ' ... \n\n')
        return

    def paywall_bypass(self, website):
        site_raw = requests.get(website).text
        source = website.split('.')[1]

        # make it and article object
        new_article = Article(site_raw, source)

        return new_article

    # customize function for each one
    def headline_grab_washpost(self):
        website = WEBSITES[0]
        # website = home
        # find websites
        site_raw = requests.get(website)
        site_soup = bs(site_raw.text, "html.parser")

        # finds headlines
        titles = site_soup.find_all('h2')
        titles.append(site_soup.find('h1'))

        headlines = {self.href_extractor(headline) for headline in titles}

        return headlines

    def headline_grab_nyt(self):
        website = WEBSITES[1]
        # website = home
        # find websites
        site_raw = requests.get(website)
        site_soup = bs(site_raw.text, "html.parser")

        # finds headlines
        titles = site_soup.find_all('article')
        headlines = {f"{website}{self.href_extractor(headline)}" for headline in titles}

        return headlines

    def headline_grab_econ(self):
        website = WEBSITES[2]
        # website = home
        # find websites
        site_raw = requests.get(website)
        site_soup = bs(site_raw.text, "html.parser")

        # finds headlines
        titles = site_soup.find_all('h3')

        # make headlines a set of tuples
        headlines = {f"{website}{self.href_extractor(headline)}" for headline in titles}

        return headlines

    def href_extractor(self, tag):
        try:
            href = tag.find('a')['href']
        except TypeError:
            return None
        return href

    # add this many random articles by getting all the headlines and exporting a random selection
    def grab_random(self, max_count):
        headlines = list(self.headline_grab_nyt() | self.headline_grab_econ() | self.headline_grab_washpost())

        # remove nonetype from return (only if it exists)
        try:
            headlines.remove(None)
        except KeyError:
            pass
        except ValueError:
            pass

        # shuffle them
        random.shuffle(headlines)

        # remove headlines with nonetypes in them
        exportable = []
        for headline in headlines:
            if not ('None' == headline.split('/')[-1].strip()):
                exportable.append(headline)

        # make sure that the shuffled versions are evenly distributed across sources
        selections = headlines[:max_count]
        sources = {headline.split('.')[1] for headline in headlines}

        while len(sources) == 1:
            random.shuffle(headlines)
            selections = headlines[:max_count]
            sources = {headline.split('.')[1] for headline in headlines}

        articles = [self.paywall_bypass(headline) for headline in selections]

        # return the amount given a max count
        return articles


def main(amount):
    # get the amount of articles inputted
    scraper = Scraper()
    exporter = Exporter()

    articles = scraper.grab_random(amount)

    exporter.create_folder()

    for article in articles:
        exporter.add_article(article)

    return exporter.folder


# printing function to let user know what is happening
if __name__ == '__main__':
    amount = int(input('How many articles do you want to read?\n'))

    folder = main(amount)

    print(f"Added {amount} articles to {folder}")


'''
NOTES
- make everything export to a new folder using an Exporter class
- use a class to automatically format the beautiful soup into an article
-
'''
