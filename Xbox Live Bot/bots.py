from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

LOGIN = 'https://login.live.com/login.srf'
XBOX_SITE = 'https://account.xbox.com/en-US/social?xr=shellnav'
XBOX_HOME = 'https://www.xbox.com/en-US/'


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
        self.driver.get(LOGIN)
        time.sleep(2)

        # send the email to the input box
        email_box = self.driver.find_element_by_xpath('//input[@type="email"]')
        email_box.send_keys(self.email)

        # click next
        next_button = self.driver.find_element_by_xpath('//input[@type="submit"]')
        next_button.click()
        time.sleep(2)

        # enter the password
        password_box = self.driver.find_element_by_xpath('//input[@type="password"]')
        password_box.send_keys(self.password)

        # click sign in
        sign_in_button = self.driver.find_element_by_xpath('//input[@type="submit"]')
        sign_in_button.click()
        time.sleep(2)

    def enter_xbox_homepage(self):
        self.driver.get(XBOX_SITE)
        time.sleep(5)

        # more code could go here in the future if it is necessary to navigate the xbox home page manually

    def get_recents(self, max_recents):
        # click recent friends tab
        friends_tab = self.driver.find_element_by_xpath('//a[@class="c-glyph glyph-people"]')
        friends_tab.click()
        time.sleep(2)

        # get recent friends by changing the tab
        friend_type_button = self.driver.find_element_by_xpath('//button[@class="c-action-trigger"]')
        friend_type_button.click()
        time.sleep(1)
        recent_players_button = self.driver.find_element_by_xpath('//button[@id="RecentPlayers"]')
        recent_players_button.click()
        time.sleep(5)  # a lot of sleep is required here as it could potentially lag

        # get the recents
        recents_raw = self.driver.find_elements_by_xpath('//ul//span[@class="name"]')[:max_recents + 1]
        recents = [tag.text for tag in recents_raw]

        return recents

    def scrape(self, max_recents):
        self.create_webdriver()

        self.login()

        self.enter_xbox_homepage()

        recents = self.get_recents(max_recents)

        self.close_webdriver()

        return recents

    def close_webdriver(self):
        self.driver.close()
