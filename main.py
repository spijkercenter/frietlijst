import datetime
import functools
from typing import List, Dict

from flask import render_template
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class Item:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class Order:
    def __init__(self, value: List[str]):
        self.name = _anonymize_name(value[1])
        self.items = [v for v in value[2:] if v]


class DTO:
    def __init__(self):
        self.__applicants: List[str] = []
        self.__items: Dict[str, int] = {}
        self.__orders: List[Order] = []

    def process_value(self, value: List[str]) -> None:
        # applications
        self.__applicants.append(_anonymize_name(value[1]))
        # items
        for item in value[2:]:
            if item:
                item_name = item.lower().strip()
                if item_name in self.__items:
                    self.__items[item_name] += 1
                else:
                    self.__items[item_name] = 1
        # orders
        self.__orders.append(Order(value))

    @property
    def items(self) -> List[Item]:
        return sorted([Item(name, amount) for name, amount in self.__items.items()],
                      key=functools.cmp_to_key(_compare_items))

    @property
    def applicants(self) -> List[str]:
        return sorted(self.__applicants)

    @property
    def orders(self) -> List[Order]:
        return sorted(self.__orders, key=lambda o: o.name)


_SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

_SHEET_ID = "18vCgc5DGUiFZN1NX_GBmxSBCb47KdsBkV6Glf9Sx-wE"
_RANGE = 'Friet bestelling!A2:F'

_cache_moment = datetime.datetime.now() - datetime.timedelta(days=1)
_cache_value = DTO()


def process(_) -> str:
    global _cache_value
    global _cache_moment

    rerun_if_later_than = _cache_moment + datetime.timedelta(seconds=10)
    now = datetime.datetime.now()
    if now > rerun_if_later_than:
        _cache_value = _get_data()
        _cache_moment = datetime.datetime.now()
    return render_template('frietlijst.html', dto=_cache_value)


def _is_friet(item: Item):
    return 'friet' in item.name or 'twister' in item.name


def _compare_items(lhs: Item, rhs: Item) -> int:
    if _is_friet(lhs) and not _is_friet(rhs):
        return -1
    elif _is_friet(rhs) and not _is_friet(lhs):
        return 1
    elif lhs.name > rhs.name:
        return 1
    else:
        return -1


def _anonymize_name(name: str) -> str:
    parts = name.split(" ")
    result = parts[0]
    for part in parts[1:]:
        if part:
            result += " " + part[0]
    return result


def _get_data() -> DTO:
    credentials: Credentials = Credentials.from_service_account_file('token.json', scopes=_SCOPES)

    service = build('sheets', 'v4', credentials=credentials)
    sheets = service.spreadsheets()
    result = sheets.values().get(spreadsheetId=_SHEET_ID, range=_RANGE).execute()
    values = result.get('values', [])

    cutoff = datetime.datetime.now() - datetime.timedelta(days=4)

    result = DTO()

    for value in values:
        if value:
            moment = datetime.datetime.strptime(value[0], '%d-%m-%Y %H:%M:%S')
            if moment > cutoff:
                result.process_value(value)

    return result
