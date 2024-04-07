from dataclasses import dataclass


@dataclass
class Account:
    email: str
    password: str
    posts_count: int
    is_work: bool


@dataclass
class Task:
    link: str
    is_finished: bool
    account: Account
    is_account_in_group: bool
    banner_link: str
    text: str

