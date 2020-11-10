from selenium import webdriver
import random
import time

# set sleep time
MIN_SLEEP_TIME = 600
MAX_SLEEP_TIME = 6000

# set click time
MIN_CLICK_TIME = 5
MAX_CLICK_TIME = 120


def visit_porn():
    driver = webdriver.Chrome()

    driver.get('https://pornhub.com')

    while True:
        time.sleep(random.randint(MIN_CLICK_TIME, MAX_CLICK_TIME))
        try:
            refs = driver.find_elements_by_xpath('//a')
            refs[0].click()
            random.shuffle(refs)
        except Exception as e:
            print(e)
            break


if __name__ == '__main__':
    while True:
        time.sleep(random.randint(MIN_SLEEP_TIME, MAX_SLEEP_TIME))
        visit_porn()
