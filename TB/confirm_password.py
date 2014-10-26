#! /usr/bin/python


from time import sleep
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from utily import web_wait, WrongPassword

class CaptCode(Exception):
    pass

def main():
    with open('config.txt') as f:
        source, password, timeout = f.read().strip().split('\n')[:3]

    try:
        with open(source) as f:
            for i, line in enumerate(f):
                line = line.rstrip()
                if len(line) == 0:
                    continue

                username = line.split('|')[0]
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
                        lf = driver.find_element_by_id('l_f_code')
                        if lf.get_attribute('class') == 'field field-checkcode ph-focus':
                            raise CaptCode
                        raise WrongPassword

                except WrongPassword:
                    print("密码不正确")
                    with open('WrongPassword.txt', 'a') as f:
                        f.write(line + '\n')
                except WebDriverException:
                    print("其他错误")
                    with open('OtherFail.txt', 'a') as f:
                        f.write(line + '\n')
                finally:
                    sleep(2)
                    driver.quit()
    except KeyboardInterrupt:
        print("用户中止")
    else:
        print('{0} 所有已完成 {0}'.format('-' * 10))
    finally:
        if i > 0:
            with open(source) as f:
                lines = f.readlines()
            with open(source, 'w') as f:
                f.writelines(lines[i:])


if __name__ == '__main__':
    main()
