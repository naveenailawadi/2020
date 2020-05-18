from pywebcopy import save_webpage
import logging
import os

# get rid of logging
logging.basicConfig()

# download website
website = input('URL for webpage to be copied: \n')
# set a directory to work in
directory = os.getcwd()

# set project name
name = input('Name of folder with page: \n')


# save the webpage (uncomment later, it is already saved)
save_webpage(url=website, project_folder=directory, project_name=name)

# get a list of the files and append to set
html_files = []
scraped_website_folder = f"{directory}/{name}"
