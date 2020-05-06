from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.api.provider.profile import ProfileProvider
from xboxapi.client import Client
import requests
import time

LOGIN = 'https://login.live.com/login.srf'
XBOX_SITE = 'https://account.xbox.com/en-US/social?xr=shellnav'
XBOX_HOME = 'https://www.xbox.com/en-US/'
MESSAGING_URL = 'https://account.xbox.com/en-us/SkypeMessages'


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

    def send_message(self, gamertag, message):
        # click the correct account
        try:
            account = self.driver.find_element_by_xpath(f'//strong[@class="topic"][text()="{gamertag}"]')
        except NoSuchElementException:
            print(f"Unable to send message to {gamertag} (account not found)")
            return False
        account.click()
        time.sleep(3)

        # send the message to the message bar
        message_bar = self.driver.find_element_by_xpath('//input[@id="newmessageinput"]')
        message_bar.send_keys(message)

        # click send
        send_button = self.driver.find_element_by_xpath('//button[@id="newmessage"]')
        send_button.click()
        time.sleep(1)

        print(f"Message sent to {gamertag}")
        return True

    def send_messages(self, gamertags, message):
        # navigate to the xbox home
        self.driver.get(MESSAGING_URL)
        time.sleep(5)

        # for testing only
        gamertags = ['LaxShaan04']

        messaged_gamers = []

        for gamer in gamertags:
            sent = self.send_message(gamer, message)
            if sent:
                messaged_gamers.append(gamer)

        return messaged_gamers

    def scrape_and_send(self, max_recents, message):
        self.create_webdriver()

        self.login()

        self.enter_xbox_homepage()

        recents = self.get_recents(max_recents)

        messaged_gamers = self.send_messages(recents, message)

        self.close_webdriver()

        return messaged_gamers

    def close_webdriver(self):
        self.driver.close()


# this class will work when microsoft fixes this endpoint
class MicrosoftMessenger:
    def __init__(self, email, password):
        self.auth_mgr = AuthenticationManager()

        # set data for auth manager
        self.auth_mgr.email_address = email
        self.auth_mgr.password = password

        # authentication
        self.auth_mgr.authenticate(do_refresh=True)

        # set the new info to a xbl client
        self.xbl_client = XboxLiveClient(
            self.auth_mgr.userinfo.userhash, self.auth_mgr.xsts_token.jwt, self.auth_mgr.userinfo.xuid)

    # sends message to list of multiple users
    def send_message(self, message, users):
        response = self.xbl_client.message.send_message(message, gamertags=users)

        return response


# create a class that uses the third party API to send messages
class XMessenger:
    def __init__(self, email, password, x_auth_key):
        self.x_auth_key = x_auth_key
        self.url = 'http://xapi.us/v2'
        self.client = Client(api_key=x_auth_key)

        # use the microsoft api to get the xuid info without using requests
        self.auth_mgr = AuthenticationManager()

        # set data for auth manager
        self.auth_mgr.email_address = email
        self.auth_mgr.password = password

        # authentication
        self.auth_mgr.authenticate(do_refresh=True)

        # set the new info to a xbl client
        self.xbl_client = XboxLiveClient(
            self.auth_mgr.userinfo.userhash, self.auth_mgr.xsts_token.jwt, self.auth_mgr.userinfo.xuid)

        self.profile_provider = ProfileProvider(self.xbl_client)

    def send_messages_url(self, gamertags, message):
        endpoint = f"{self.url}/messages"
        headers = {
            'X-Auth': self.x_auth_key,
            'Content-Type': 'application/json'
        }

        # convert the gamertags to xuids
        xuids = [self.get_xuid(gamertag) for gamertag in gamertags]

        body = {
            "to": xuids,
            "message": message
        }

        response = requests.post(url=endpoint, data=body, headers=headers)

        return response

    def send_message(self, gamertag, message):
        # create a game object
        gamer = self.client.gamer(gamertag)

        # send the message
        gamer.send_message(message)

    def get_xuid(self, gamertag):
        profile = self.profile_provider.get_profile_by_gamertag(gamertag).json()
        xuid = profile['profileUsers'][0]['id']

        return xuid
