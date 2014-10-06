#! /usr/bin/python

from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException


def wait(wait_func):
    try:
        WebDriverWait(driver, 10).until(wait_func)
    except TimeoutException:
        print('time out')

with open('newpassword.txt') as f:
    newpassword = f.read().strip()

with open('1.txt') as f:
    for i, line in enumerate(f):
        if i % 5 == 0:
            sleep(60)

        username, password = line.split('|')[:2]
        print(str(i + 1), username)

        driver = webdriver.Chrome('./chromedriver')
        driver.get('https://login.taobao.com/member/login.jhtml')
        wait(lambda the_driver: the_driver.find_element_by_id('TPL_username_1'))
        driver.find_element_by_id('TPL_username_1').send_keys(username)
        driver.find_element_by_id('TPL_password_1').send_keys(password)
        driver.find_element_by_id('J_SubmitStatic').click()

        wait(lambda the_driver: the_driver.find_element_by_id('J_MtMainNav'))

        driver.get('http://member.1688.com/member/account_security.htm')

        wait(lambda the_driver: the_driver.find_element_by_id('security_product'))
        driver.find_element_by_id('security_product')\
            .find_element_by_tag_name('table')\
            .find_element_by_tag_name('tbody')\
            .find_elements_by_tag_name('tr')[1]\
            .find_elements_by_tag_name('td')[3]\
            .find_element_by_tag_name('a').click()

        wait(lambda the_driver: the_driver.find_element_by_id('oldPassword'))
        driver.find_element_by_id('oldPassword').send_keys(password)
        try:
            driver.find_element_by_id('newPassword').send_keys(newpassword)
        except WebDriverException:
            driver.find_element_by_id('newPassword').send_keys(newpassword)

        driver.find_element_by_id('confirmPassword').send_keys(newpassword)
        driver.find_element_by_id('modifyPassword')\
            .find_element_by_tag_name('table')\
            .find_element_by_tag_name('tbody')\
            .find_elements_by_tag_name('tr')[3]\
            .find_elements_by_tag_name('td')[1]\
            .find_element_by_tag_name('input').click()

        sleep(5)
        driver.quit()

print('All Done')
