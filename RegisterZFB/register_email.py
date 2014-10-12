#! /usr/bin/python

import os
import string
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException, ElementNotVisibleException
from subprocess import check_output, CalledProcessError
from PIL import ImageGrab

def generate_username_and_password():
    random.seed()
    username = string.letters[random.randint(0, len(string.letters)-1)]
    values = string.letters + string.digits
    for i in range(6):
        username += values[random.randint(0, len(values) - 1)]
    return username, username * 2

def captchar_code(png, codetype):
    dama_username = 'lunbest'
    dama_password = '789837'
    try:
        return check_output(['DecodeCaptChar.exe', png, dama_username, dama_password, str(codetype)])
    except CalledProcessError:
        return ''

def main():
    def wait(wait_func, timeout=10):
        try:
            WebDriverWait(driver, timeout).until(wait_func)
            return True
        except TimeoutException:
            return False


    try:
        driver = webdriver.Chrome('./chromedriver')
        driver.get('http://reg.email.163.com/unireg/call.do?cmd=register.entrance')

        wait(lambda the_driver: the_driver.find_element_by_xpath('//*[@id="tabsUl"]/li[1]/a'))
        while True:
            try:
                driver.find_element_by_id('nameIpt').send_keys('')
                break
            except ElementNotVisibleException:
                sleep(1)
                driver.find_element_by_xpath('//*[@id="tabsUl"]/li[1]/a').click()

        png = 'q.png'
        im = ImageGrab.grab((413, 583, 536, 633))
        im.save(png, 'png')

        code = captchar_code(png, 54)
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
        wait(waitNext, 10000)

        try:
            confirm = driver.find_element_by_id('gvcodeIpt')
            sleep(2)
            im = ImageGrab.grab((432, 455, 683, 483))
            im.save(png, 'png')
            code = captchar_code(png, 73)
            driver.find_element_by_id('gvcodeIpt').send_keys(code.decode('gbk'))
            driver.find_element_by_id('gsubmitA').click()
            wait(lambda the_driver: the_driver.find_element_by_id('_mail_tabitem_0_34text'), 10000)
        except WebDriverException:
            pass

        def is_success():
            try:
                return driver.find_element_by_id('_mail_tabitem_0_34text')
            except WebDriverException:
                try:
                    return driver.find_element_by_xpath('//*[@id="secondarySection"]/div/p[1]')
                except WebDriverException:
                    return None

        if is_success():
            sleep(5)
            print(username)
            with open('163.txt', 'a') as f:
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
