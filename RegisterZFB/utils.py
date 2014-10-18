import string
import random
import re
from time import sleep
from subprocess import check_output, CalledProcessError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from PIL import ImageGrab
import urllib
import urllib2
import json


def web_wait(driver, wait_func, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(wait_func)
        return True
    except TimeoutException:
        return False


def captchar_code(png, codetype):
    with open('mm.json') as f:
        keys = json.load(f)
        dama_username = keys['dama2_user']
        dama_password = keys['dama2_pw']
    try:
        return check_output(['DecodeCaptChar.exe', png, dama_username, dama_password, str(codetype)])
    except CalledProcessError:
        return ''


def generate_username_and_password():
    random.seed()
    username = string.letters[random.randint(0, len(string.letters)-1)]
    values = string.letters + string.digits
    for i in range(6):
        username += values[random.randint(0, len(values) - 1)]
    return username, username[::-1] + username


def grab_image(x1, y1, x2, y2):
    png = 'q.png'
    im = ImageGrab.grab((x1, y1, x2, y2))
    im.save(png, 'png')
    return png


def __request_data(data):
    req = urllib2.Request(url='http://api.f02.cn/http.do', data=urllib.urlencode(data))
    res = urllib2.urlopen(req)
    return res.read()


def __request_login():
    return __request_data({'action': 'loginIn', 'uid': 'tigerpoon', 'pwd': 'poon1984'})


def get_mobile(pid):
    res_login = __request_login()
    data_getmobile = dict(zip(('uid', 'token'), res_login.split('|')))
    data_getmobile['action'] = 'getMobilenum'
    data_getmobile['pid'] = pid
    res_getmobile = __request_data(data_getmobile)
    return res_getmobile.split('|')[0]


def get_mobile_code(mobile):
    res_login = __request_login()
    data_getcode = dict(zip(('uid', 'token'), res_login.split('|')))
    data_getcode['action'] = 'getVcodeAndReleaseMobile'
    data_getcode['mobile'] = mobile
    while True:
        res_getcode = __request_data(data_getcode)
        if res_getcode[:11].isdigit():
            a = re.findall(r'\d{6}', res_getcode.split('|')[1])
            return a[0]
        sleep(1)
