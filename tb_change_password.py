#! /usr/bin/python

from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException


class WrongPassword(Exception): pass

def wait(wait_func):
    try:
        WebDriverWait(driver, int(timeout)).until(wait_func)
        return True
    except TimeoutException:
        return False

with open('config.txt') as f:
    source, newpassword, timeout = f.read().strip().split('\n')[:3]

with open(source) as f:
    for i, line in enumerate(f):
        line = line.strip()
        if len(line) == 0:
            continue

        username, password = line.split('|')[:2]
        print(str(i + 1), username)

        try:
            driver = webdriver.Chrome('./chromedriver')
            while True:
                driver.get('https://login.taobao.com/member/login.jhtml')
                if wait(lambda the_driver: the_driver.find_element_by_id('TPL_username_1')):
                    break

            try:
                safeLoginCheck = driver.find_element_by_id('J_SafeLoginCheck')
                if safeLoginCheck.is_selected():
                    safeLoginCheck.click()
                    sleep(0.5)
            except WebDriverException:
                pass

            driver.find_element_by_id('TPL_username_1').send_keys(username)
            driver.find_element_by_id('TPL_password_1').send_keys(password)
            driver.find_element_by_id('J_SubmitStatic').click()

            if not wait(lambda the_driver: the_driver.find_element_by_id('J_MtMainNav')):
                raise WrongPassword

            driver.get('http://member.1688.com/member/account_security.htm')

            wait(lambda the_driver: the_driver.find_element_by_id('security_product'))
            driver.find_element_by_xpath('//*[@id="security_product"]/table/tbody/tr[2]/td[4]/a').click()

            if not wait(lambda the_driver: the_driver.find_element_by_id('oldPassword')):
                driver.get('http://110.taobao.com/account/modify_pwd.htm')
                wait(lambda the_driver: the_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div/div/div[2]/a[1]'))
                driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div/div/div[2]/a[1]').click()
                wait(lambda the_driver: the_driver.find_element_by_id('J_old_password_input'))
                driver.find_element_by_id('J_old_password_input').send_keys(password)
                driver.find_element_by_id('J_password_input').send_keys(newpassword)
                driver.find_element_by_id('J_repassword_input').send_keys(newpassword)
                driver.find_element_by_xpath('//*[@id="J_modify_password_form"]/div[4]/button').click()
            else:
                driver.find_element_by_id('oldPassword').send_keys(password)
                try:
                    driver.find_element_by_id('newPassword').send_keys(newpassword)
                except WebDriverException:
                    driver.find_element_by_id('newPassword').send_keys(newpassword)

                driver.find_element_by_id('confirmPassword').send_keys(newpassword)
                driver.find_element_by_xpath('//*[@id="modifyPassword"]/table/tbody/tr[4]/td[2]/input').click()
        except WrongPassword:
            with open('WrongPassword.txt', 'a') as f:
                print(line, file=f)
        except WebDriverException:
            with open('OtherFail.txt', 'a') as f:
                print(line, file=f)
        finally:
            sleep(2)
            driver.quit()

print('{0} All Done {0}'.format('-' * 10))
