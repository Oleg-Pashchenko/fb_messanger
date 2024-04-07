import random
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from app.google_database.image import download_image
from app.google_database.models import *
from app.google_database.tasks import get_task

POSTER_URL = 'https://www.facebook.com/'
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(chrome_options)

def auth(email: str, password: str):
    driver.find_element(By.ID, 'email').send_keys(email)
    driver.find_element(By.ID, 'pass').send_keys(password)
    driver.find_element(By.ID, 'loginbutton').click()


def random_scroll():
    page_height = driver.execute_script("return document.body.scrollHeight")
    scroll_amount = 0

    for _ in range(random.randint(3, 10)):
        scroll_new = random.randint(page_height // 4, page_height // 2)
        for _ in range(10):
            scroll_amount += scroll_new / 10
            driver.execute_script("window.scrollTo(0, {})".format(scroll_amount))
            time.sleep(0.1)
        time.sleep(random.randint(3, 6))


def create_post():
    span = driver.find_element(By.XPATH, "//span[text()='Напишите что-нибудь...']")
    span.click()
    time.sleep(1)
    span = driver.find_element(By.XPATH, "//div[@aria-label='Напишите что-нибудь...']")
    time.sleep(1)
    span.send_keys('Текст перегенерированный нейронкой')
    time.sleep(1)
    try:
        span.send_keys(Keys.COMMAND, 'v')
    except:
        pass
    span.send_keys(Keys.CONTROL, 'v')
    time.sleep(2)
    # driver.find_element(By.XPATH, "//div[@aria-label='Отправить']").click()

def start(task: Task):

    download_image(task.banner_link)

    driver.get(POSTER_URL)
    auth(task.account.email, task.account.password)
    random_scroll()
    driver.get('https://www.facebook.com/groups/220285938305816')
    random_scroll()
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(3)
    create_post()

    driver.close()


def cycle():
    while True:
        task = get_task()
        start(task)


cycle()

