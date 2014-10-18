#! /usr/bin/python

import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException, ElementNotVisibleException
from utils import web_wait, grab_image, captchar_code, generate_username_and_password

with open('mm.json') as f:
    keys = json.load(f)
    query_password = keys['query_pw']
    pay_password = keys['pay_pw']


def main():
    with open('zfb') as f, open('ID.txt') as fid:
        for line in f:
            line = line.rstrip()
            print(line)
            username, password = line.split('|')
            try:
                driver = webdriver.Chrome('./chromedriver')
                driver.get('http://mail.163.com/')

                web_wait(driver, lambda the_driver: the_driver.find_element_by_id('idInput'))
                driver.find_element_by_id('idInput').send_keys(username + '@163.com')
                driver.find_element_by_id('pwdInput').send_keys(password)
                driver.find_element_by_id('loginBtn').click()

                web_wait(driver, lambda the_driver: the_driver.find_element_by_id('_mail_component_51_51'))
                driver.find_element_by_id('_mail_component_51_51').click()

                first_email_xpath = '//*[@id="_dvModuleContainer_mbox.ListModule_0"]/div/div/div[4]/div[2]/div/div[1]/div[2]/span'
                if web_wait(driver, lambda the_driver: the_driver.find_element_by_xpath(first_email_xpath)):
                    driver.find_element_by_xpath(first_email_xpath).click()

                    while True:
                        sleep(1)
                        zfb_email = re.search(r'"(read/readhtml[^"]+)"', driver.page_source)
                        if zfb_email:
                            driver.get('http://mail.163.com/js6/' + zfb_email.group(1).replace('&amp;', '&'))
                            sleep(1)
                            zfb_link = re.search(r'"(https://lab.alipay.com/user/activeUserValid.htm[^"]+)"', driver.page_source)
                            if zfb_link:
                                driver.get(zfb_link.group(1).replace('&amp;', '&'))
                                if web_wait(driver, lambda the_driver: the_driver.find_element_by_id('queryPwd')):
                                    driver.find_element_by_id('queryPwd').send_keys(query_password)
                                    driver.find_element_by_id('queryPwdConfirm').send_keys(query_password)
                                    driver.find_element_by_id('payPwd').send_keys(pay_password)
                                    driver.find_element_by_id('payPwdConfirm').send_keys(pay_password)
                                    realName, IDCardNo = fid.readline().split('----')
                                    driver.find_element_by_id('realName').send_keys(realName.decode('gbk'))
                                    driver.find_element_by_id('IDCardNo').send_keys(IDCardNo)
                                    if web_wait(driver, lambda the_driver: the_driver.find_element_by_id('J_CardHolderName')):
                                        driver.find_element_by_id('J_submit')
                                    with open('zfb_done', 'a') as fzfb:
                                        fzfb.write(line + '\n')
                                sleep(3)
                            break
            finally:
                driver.quit()

import sys
if __name__ == '__main__':
    main()
