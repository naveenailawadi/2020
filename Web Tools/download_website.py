from pywebcopy import save_website
import logging
import os

# get rid of logging
logging.basicConfig()

# download website
website = input('URL for website to be copied: \n')
# set a directory to work in
directory = os.getcwd()

# set project name
name = input('What do you want to name the folder with the information?\n')

# save the webpage (uncomment later, it is already saved)
save_website(url=website, project_folder=directory, project_name=name)

# get a list of the files and append to set
html_files = []
scraped_website_folder = f"{directory}/{name}"
