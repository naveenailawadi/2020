from pywebcopy import WebPage
import logging
import os


logging.basicConfig()

# set the urls for downloading
sites = ['https://www.entredeveloperslab.com/', 'https://www.entredeveloperslab.com/testimonials', 'https://www.entredeveloperslab.com/tune-in', 'https://www.entredeveloperslab.com/wine-juicer']

# set a directory to work in
directory = 'home'

os.chdir(directory)

# save the webpage (uncomment later, it is already saved)
for site in sites:
    wp = WebPage()
    wp.get(site)
    wp.save_complete()
