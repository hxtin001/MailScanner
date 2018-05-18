# -*- coding: utf-8 -*-
import time
from selenium import webdriver
# from pyvirtualdisplay import Display
import logging.handlers
from selenium.webdriver.common.keys import Keys
import constants
import json

# For display none
# display = Display(visible=True, size=(constants.screen_width_default, constants.screen_height_default))
# display.start()

# For chrome
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_handle = logging.handlers.TimedRotatingFileHandler(constants.path_application_log, when='midnight')
# log_handle = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] - [%(filename)s:%(lineno)s]- %(levelname)s - %(message)s')
log_handle.setFormatter(formatter)
logger.addHandler(log_handle)

class GetMail:

    driver = None
    config = None
    case = None

    def __init__(self, config, case):
        logger.info('----------------------------START--------------------------------')
        self.config = config
        self.case = case
        try:
            self.driver = webdriver.Chrome(self.config.get('DRIVER_PATH'))
            self.driver.get(self.case.get('URL'))
            self.driver.implicitly_wait(100)
            logger.info("Connected to {}".format(self.case.get('URL')))
        except Exception as e:
            logger.info('Can not connect to website. Error: {}.'.format(e))
            raise e


    def executer(self):
        try:
            mail_links = self.driver.find_elements_by_css_selector(self.case.get('MAIL_LIST_CSS_SELECTOR'))
            mail_href = []
            for mail_link in mail_links:
                mail_href.append(mail_link.get_attribute('href'))
                time.sleep(0.5)

            for href in mail_href:
                self.driver.get(href)
                logger.info('Go to: '.format(href))
                time.sleep(5)
                emails = self.driver.find_element_by_css_selector(self.case.get('MAIL_CSS_SELECTOR'))
                self.mail_filter(emails.text)

        except Exception as e:
            self.driver.close()
            logger.info('Step 1 error: {}'.format(e.message))
            raise e

    def run(self):
        paginations = self.driver.find_elements_by_css_selector(self.case.get('PAGINATION_CSS_SELECTOR'))
        page_href = []
        for page in paginations:
            page_href.append(page.get_attribute('href'))
            time.sleep(0.5)

        for href in page_href:
            self.driver.get(href)
            logger.info('Go to: '.format(href))
            time.sleep(5)
            self.executer()


    def mail_filter(self, emails=''):
        mails = []
        for mail in emails.splitlines():
            if mail:
                mail = mail.strip()
                if (mail != '') and (self.config.get('FILTER_BY') in mail):
                    mails.append(mail)
        if not mails:
            logger.info("Cannot find any hotmail here")
        print mails


def load_data_json(fileName='data2.json'):
    with open(fileName) as json_data:
        data = json.load(json_data)
    return data.get("CONFIG"), data.get("CASES")

def _main():
    config, cases = load_data_json()
    for case in cases:
        GetMail(config, case).run()

if __name__ == '__main__':
    _main()







