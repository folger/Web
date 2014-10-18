#! /usr/bin/python

from time import sleep
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, ElementNotVisibleException
from utils import web_wait, grab_image, captchar_code, generate_username_and_password


def main():
    try:
        driver = webdriver.Chrome('./chromedriver')
        driver.get('http://reg.email.163.com/unireg/call.do?cmd=register.entrance')

        web_wait(driver, lambda the_driver: the_driver.find_element_by_xpath('//*[@id="tabsUl"]/li[1]/a'))
        while True:
            try:
                driver.find_element_by_id('nameIpt').send_keys('')
                break
            except ElementNotVisibleException:
                sleep(1)
                driver.find_element_by_xpath('//*[@id="tabsUl"]/li[1]/a').click()

        code = captchar_code(grab_image(380, 550, 536, 633), 54)
        username, password = generate_username_and_password()
        driver.find_element_by_id('nameIpt').send_keys(username)
        sleep(1)
        driver.find_element_by_id('mainPwdIpt').send_keys(password)
        sleep(1)
        driver.find_element_by_id('mainCfmPwdIpt').send_keys(password)
        sleep(1)
        driver.find_element_by_id('vcodeIpt').send_keys(code)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="mainRegA"]').click()
        sleep(2)

        def waitNext(the_driver):
            try:
                return the_driver.find_element_by_id('gvcodeIpt')
            except WebDriverException:
                return the_driver.find_element_by_xpath('//*[@id="secondarySection"]/div/p[1]')
        web_wait(driver, waitNext, 10000)

        try:
            confirm = driver.find_element_by_id('gvcodeIpt')
            sleep(2)
            code = captchar_code(grab_image(400, 420, 683, 483), 73)
            confirm.send_keys(code.decode('gbk'))
            sleep(1)
            driver.find_element_by_id('gsubmitA').click()
            web_wait(driver, lambda the_driver: the_driver.find_element_by_id('dvMultiTabWrapper'), 10000)
        except WebDriverException:
            pass

        def is_success():
            try:
                return driver.find_element_by_id('dvMultiTabWrapper')
            except WebDriverException:
                try:
                    return driver.find_element_by_xpath('//*[@id="secondarySection"]/div/p[1]')
                except WebDriverException:
                    return None

        if is_success():
            sleep(5)
            print(username)
            with open('163', 'a') as f:
                f.write('|'.join([username, password]) + '\n')
        else:
            print('Fail ...')
    finally:
        driver.quit()

import sys
if __name__ == '__main__':
    times = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for i in range(times):
        main()
