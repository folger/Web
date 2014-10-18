#! /usr/bin/python

from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException, ElementNotVisibleException
from utils import web_wait, grab_image, captchar_code, generate_username_and_password, get_mobile, get_mobile_code


def main():
    with open('163') as f:
        for line in f:
            line = line.rstrip()
            print(line)
            username, password = line.split('|')
            try:
                driver = webdriver.Chrome('./chromedriver')
                driver.get('https://memberprod.alipay.com/account/reg/email.htm')

                web_wait(driver, lambda the_driver: the_driver.find_element_by_id('J-checkcode-img'))
                code = captchar_code(grab_image(379, 550, 572, 600), 42)
                driver.find_element_by_id('J-accName').send_keys(username + '@163.com')
                driver.find_element_by_id('J-checkcode').send_keys(code)
                driver.find_element_by_id('J-submit').click()

                if web_wait(driver, lambda the_driver: the_driver.find_element_by_xpath('/html/body/div[8]/div[2]/iframe')):
                    sleep(3)
                    iframe = driver.find_element_by_xpath('/html/body/div[8]/div[2]/iframe')
                    driver.get(iframe.get_attribute('src'))
                    if web_wait(driver, lambda the_driver: the_driver.find_element_by_id('J-secure-mobile')):
                        while True:
                            mobile = get_mobile('1245')
                            driver.find_element_by_id('J-secure-mobile').send_keys(mobile)
                            driver.find_element_by_id('J-getCheckcodeBtn').click()
                            if web_wait(driver, lambda the_driver: the_driver.find_element_by_id('J-checkcode'), 3):
                                break
                        code = get_mobile_code(mobile)
                        driver.find_element_by_id('J-checkcode').send_keys(code)
                        driver.find_element_by_id('J-submit-btn').click()
                        sleep(5)
                        with open('zfb', 'a') as fzfb:
                            fzfb.write(line + '\n')
            finally:
                driver.quit()


import sys
if __name__ == '__main__':
    main()
