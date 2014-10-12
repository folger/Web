#! /usr/bin/python

import string
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException


def main():
    def wait(wait_func):
        try:
            WebDriverWait(driver, 10).until(wait_func)
            return True
        except TimeoutException:
            return False

    with open('163.txt') as f:
        for line in f:
            line = line.rstrip()
            username, password = line.split('|')
            try:
                driver = webdriver.Chrome('./chromedriver')
                driver.get('http://mail.163.com')

                wait(lambda the_driver: the_driver.find_element_by_id('idInput'))
                driver.find_element_by_id('idInput').send_keys(username)
                driver.find_element_by_id('pwdInput').send_keys(password)
                driver.find_element_by_id('loginBtn').click()
                sleep(5)
            finally:
                driver.quit()

if __name__ == '__main__':
    main()
