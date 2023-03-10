import os
import atexit
import time

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import URL


class Scraper:
    def __init__(self):
        self.html = ''
        self.headers = Headers(browser='firefox', os='lin').generate()
        self.driver = None
        self.driver_path = ''

        atexit.register(self.terminate)

    def requests_get(self, url):
        response = requests.get(url, headers=self.headers)
        self.html = response.text

    def __driver_init(self):
        self.driver_path = GeckoDriverManager().install()
        self.__start_client()

    def __start_client(self):
        self.driver = webdriver.Firefox(executable_path=self.driver_path)

    def driver_get(self, url):
        if not self.driver:
            self.__driver_init()
        self.driver.get(url)
        self.html = self.driver.page_source

    def get_soup(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        return soup

    def terminate(self):
        if self.driver:
            self.driver.quit()

    def refresh(self):
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.CONTROL + 'r')
