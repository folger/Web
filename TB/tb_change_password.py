#! /usr/bin/python

from time import sleep
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from utily import web_wait, WrongPassword


def main():
    with open('config.txt') as f:
        source, newpassword, timeout = f.read().strip().split('\n')[:3]

    try:
        with open(source) as f:
            for i, line in enumerate(f):
                line = line.rstrip()
                if len(line) == 0:
                    continue

                username, password = line.split('|')[:2]
                print(str(i + 1), username)

                try:
                    driver = webdriver.Chrome('./chromedriver')

                    def my_web_wait(func):
                        return web_wait(driver, func, timeout)

                    while True:
                        driver.get('https://login.taobao.com/member/login.jhtml')
                        if my_web_wait(lambda the_driver: the_driver.find_element_by_id('TPL_username_1')):
                            break

                    sleep(2)
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

                    if not my_web_wait(lambda the_driver: the_driver.find_element_by_id('J_MtMainNav')):
                        raise WrongPassword

                    driver.get('http://member.1688.com/member/account_security.htm')

                    my_web_wait(lambda the_driver: the_driver.find_element_by_id('security_product'))
                    driver.find_element_by_xpath('//*[@id="security_product"]/table/tbody/tr[2]/td[4]/a').click()

                    if not my_web_wait(lambda the_driver: the_driver.find_element_by_id('oldPassword')):
                        driver.get('http://110.taobao.com/account/modify_pwd.htm')
                        my_web_wait(lambda the_driver: the_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div/div/div[2]/a[1]'))
                        driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div/div/div[2]/a[1]').click()
                        my_web_wait(lambda the_driver: the_driver.find_element_by_id('J_old_password_input'))
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
                    print("成功")
                except WrongPassword:
                    print("密码不正确")
                    with open('WrongPassword.txt', 'a') as f:
                        f.write(line + '\n')
                except WebDriverException:
                    print("其他错误")
                    with open('OtherFail.txt', 'a') as f:
                        f.write(line + '\n')
                except WebDriverException:
                        pass
                finally:
                    sleep(2)
                    driver.quit()
    except KeyboardInterrupt:
        print("用户中止")
    else:
        print('{0} 所有已完成 {0}'.format('-' * 10))


if __name__ == '__main__':
    main()
