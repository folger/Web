from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class WrongPassword(Exception):
    pass


def web_wait(driver, wait_func, timeout=10):
    try:
        WebDriverWait(driver, int(timeout)).until(wait_func)
        return True
    except TimeoutException:
        return False
