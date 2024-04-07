import random

from app.google_database.models import Account
from app.google_database.sheets import accounts


def get_random_account():
    work_accounts = []
    for account in accounts.get_all_values()[1::]:
        account = Account(*account)
        if isinstance(account.is_work, str):
            account.is_work = True
        if not account.is_work:
            continue
        work_accounts.append(account)
    return random.choice(work_accounts)


def get_account_by_email(email: str):
    for account in accounts.get_all_values()[1::]:
        account = Account(*account)
        if account.email == email:
            return account


def save_account(email, usage_count, is_work):
    account_data = accounts.get_all_values()
    for row_index, account_row in enumerate(account_data):
        if account_row[0] == email:
            accounts.update_cell(row_index + 1, 3, usage_count)
            accounts.update_cell(row_index + 1, 4, is_work)
            break

