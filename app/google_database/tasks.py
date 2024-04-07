import random

from app.google_database.accounts import get_random_account, get_account_by_email
from app.google_database.sheets import groups, banners
from app.google_database.models import *
from app.openai_connector import perephrase


def get_random_banner():
    return random.choice(banners.get_all_values()[1::])


prompt = 'Здравствуйте. Вам нужны услуги программиста?'


def get_task():
    tasks = []
    groups_data = groups.get_all_values()
    for group in groups_data[1::]:
        account = get_account_by_email(group[2])
        if account is None:
            account = get_random_account()

        task = Task(
            link=group[0],
            is_finished=group[1],
            account=account,
            is_account_in_group=group[3],
            banner_link=get_random_banner(),
            text=perephrase(prompt)
        )
        if task.is_finished == '':
            return task


def save_task(link, status, email, email_in_group):
    groups_data = groups.get_all_values()
    for row_index, group_row in enumerate(groups_data):
        if group_row[0] == link:
            groups.update_cell(row_index + 1, 1, link)
            groups.update_cell(row_index + 1, 2, status)
            groups.update_cell(row_index + 1, 3, email)
            groups.update_cell(row_index + 1, 4, email_in_group)
            break

