import time

from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import bs4
import dataclasses
from datetime import datetime, timedelta


def convert_message_time(message_time):
    current_time = datetime.now()
    if 'мин.' in message_time:
        minutes = int(message_time.split()[0])
        timestamp = current_time - timedelta(minutes=minutes)
    elif 'ч.' in message_time:
        hours = int(message_time.split()[0])
        timestamp = current_time - timedelta(hours=hours)
    elif 'д.' in message_time:
        days = int(message_time.split()[0])
        timestamp = current_time - timedelta(days=days)
    else:
        # Если формат времени не распознан, возвращаем None
        return None
    return timestamp


@dataclasses.dataclass
class Message:
    user: str
    text: str
    link: str
    timestamp: datetime


MESSNGER_URL = 'https://www.facebook.com/messages/'

driver = webdriver.Chrome()


def auth(email: str, password: str):
    time.sleep(5)
    try:
        button = driver.find_element(By.XPATH, '//button[@title="Разрешить все cookie"]')
        button.click()

    except:
        pass
    time.sleep(3)
    driver.find_element(By.ID, 'email').send_keys(email)
    driver.find_element(By.ID, 'pass').send_keys(password)
    driver.find_element(By.ID, 'loginbutton').click()


def close_alert():
    try:
        alert = driver.switch_to.alert
        alert.dismiss()  # Можно также использовать alert.accept() для принятия уведомления
    except:
        pass


def read_new_messages():
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    cards = soup.find('div', {'aria-label': 'Чаты'}).find_all('a', {'role': 'link'})
    links = ['https://www.facebook.com' + card.get('href') for card in cards]
    chat_div = driver.find_element(By.XPATH, "//div[@aria-label='Чаты']")
    chat_links = chat_div.find_elements(By.XPATH, ".//a[@role='link']")
    messages = []
    for id, link in enumerate(chat_links):
        user, message, _, message_time = map(str, link.text.split('\n'))
        is_bot_message = 'Вы:' in message
        if is_bot_message:
            continue
        message_time = convert_message_time(message_time)
        message = message.replace('Вы: ', '')
        messages.append(Message(
            user=user,
            text=message,
            link=links[id],
            timestamp=message_time
        ))
    return messages


def send_message(link, text):
    driver.get(link)
    time.sleep(7)
    element = driver.find_element(By.XPATH, "//div[@aria-label='Сообщение']")
    element.send_keys(text)
    element.send_keys(Keys.ENTER)
    time.sleep(2)


while True:
    for account in accounts:
        try:
            driver.get(MESSNGER_URL)
            auth(email, password)
            time.sleep(10)
            messages = read_new_messages()
            print(messages)
        except Exception as e:
            print('error', e)
        finally:
            driver.close()
