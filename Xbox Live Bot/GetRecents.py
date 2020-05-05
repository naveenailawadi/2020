from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

SITE = 'https://login.live.com/login.srf'


class RecentScraper:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    # function to open the driver
    def create_webdriver(self):
        # open a webdriver
        self.driver = webdriver.Firefox()
        time.sleep(2)

    # create a function login
    def login(self):
        # go to the login page
        self.driver.get(SITE)

        # send the email to the input box
        email_box = self.driver.find_element_by_xpath('//input[@type="email"]')
        email_box.send_keys(self.email)

        # click next
        next_button = self.driver.find_element_by_xpath('//input[@type="submit"]')
        next_button.click()
        time.sleep(2)

        # enter the password
        password_box = self.driver.find_element_by_xpath('//input[@type="submit"]')
        password_box.send_keys(self.password)

        # click sign in
        sign_in_button = self.driver.find_element_by_xpath('//input[@type="submit"]')
        sign_in_button.click()
        time.sleep(2)
