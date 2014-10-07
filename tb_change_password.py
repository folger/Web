#! /usr/bin/python

from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException


def wait(wait_func):
    try:
        WebDriverWait(driver, 15).until(wait_func)
        return True
    except TimeoutException:
        return False

with open('config.txt') as f:
    source, newpassword = f.read().strip().split('\n')[:2]

with open(source) as f:
    for i, line in enumerate(f):
        #if i > 0 and i % 5 == 0:
            #sleep(30)

        line = line.strip()
        username, password = line.split('|')[:2]
        print(str(i + 1), username)

        driver = webdriver.Chrome('./chromedriver')
        while True:
            driver.get('https://login.taobao.com/member/login.jhtml')
            if wait(lambda the_driver: the_driver.find_element_by_id('TPL_username_1')):
                break

        driver.find_element_by_id('TPL_username_1').send_keys(username)
        driver.find_element_by_id('TPL_password_1').send_keys(password)
        driver.find_element_by_id('J_SubmitStatic').click()

        if not wait(lambda the_driver: the_driver.find_element_by_id('J_MtMainNav')):
            driver.quit()
            with open('fail.txt', 'a') as f:
                print(line, file=f)
            continue

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

        sleep(3)
        driver.quit()

print('All Done')
