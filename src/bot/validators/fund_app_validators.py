# Валидаторы для fund_application.py
import re

from datetime import date

from ..constans import fund_app_constans as constans


def checking_not_digits(data: str) -> bool:
    """Проверка текстовых значений."""
    if (
        all(x.isalpha() or x.isspace() or
            x in constans.SPEC_SYM for x in data) and
            data != " " and len(data) < 100
    ):
        return True
    return False


def checking_phone_number(data: str) -> bool:
    """Проверка телефонного номера."""
    if data[0] == '+':
        data = data[1:]
    if data.isdigit() and len(data) == 11:
        return True
    return False


def checking_email(data: str) -> bool:
    """Проверка email."""
    return bool(re.match(constans.REGEX_EMAIL, data))


def checking_count_people_in_family(data: str) -> bool:
    """
    Проверка на число.
    Для колличества членов в семье.
    """
    if data.isdigit() and int(data) > 0 and int(data) <= 52:
        return True
    return False


def checking_birthday(data: str) -> bool:
    """Проверка правильности ввода даты рождения."""
    flag = True
    date_now = date.today()

    if bool(re.match(constans.REGEX_BIRTHDAY, data)):
        date_split_list = data.split(".")
        if (
            int(date_split_list[0]) < 1 or
            int(date_split_list[0]) > 31
        ):
            flag = False
        if (
            int(date_split_list[1]) < 1 or
            int(date_split_list[1]) > 12
        ):
            flag = False
        if (
            int(date_split_list[2]) < 1950 or
            int(date_split_list[2]) > date_now.year
        ):
            flag = False
        if (
            int(date_split_list[2]) == date_now.year and
            int(date_split_list[1]) >= date_now.month and
            int(date_split_list[0]) > date_now.day
        ):
            flag = False
    else:
        flag = False
    return flag


def checking_weight_and_height(data: str) -> bool:
    """Проверка правильности ввода веса и роста."""
    if data.isdigit() and int(data) > 0 and int(data) < 100:
        return True
    return False
