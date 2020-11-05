from headliner import get_headlines, DEFAULT_FOLDER
from datetime import datetime as dt
from emailer import MailBot
from secrets import EMAIL, PASSWORD, RECIPIENTS, ARTICLE_OUTPUT
import schedule
import shutil
import time
import os

BODY = 'Enjoy your daily news!\n\n'

# set schedule
RATES_SEND_TIME = '07:00'
DAYS = ['monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday', 'sunday']


# make a main function to run
def main(output=ARTICLE_OUTPUT):
    today = dt.now()
    print(f"Sending news for {today.month}-{today}")
    # clear the folder
    if os.path.exists(DEFAULT_FOLDER):
        shutil.rmtree(DEFAULT_FOLDER)

    # run the headliner
    get_headlines(output)

    # send the folder as a compressed zip to all the recipients
    filename = f"{DEFAULT_FOLDER}.zip"
    shutil.make_archive(DEFAULT_FOLDER, 'zip', DEFAULT_FOLDER)
    bot = MailBot(EMAIL, PASSWORD)

    # send the message
    bot.send_message(f"News {today.month}-{today.day}",
                     BODY, RECIPIENTS, zip_file=filename)


if __name__ == '__main__':
    for name in DAYS:
        statement = f"schedule.every().{name}.at(RATES_SEND_TIME).do(main)"
        exec(statement)
        print(f"Added {name}")

    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(60)
