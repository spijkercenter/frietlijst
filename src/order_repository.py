from datetime import datetime
from typing import List

from cachetools import cached, TTLCache
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from models.order import Order


class OrderRepository:
    def __init__(self,
                 sa_file_name: str,
                 spreadsheet_id: str,
                 spreadsheet_range: str,
                 ):
        credentials = Credentials.from_service_account_file(
            filename=sa_file_name,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'],
        )
        service = build('sheets', 'v4', credentials=credentials)
        self.__sheets = service.spreadsheets()
        self.__spreadsheet_id = spreadsheet_id
        self.__spreadsheet_range = spreadsheet_range

    def find_by_datetime_placed_greater_than(self, min_datetime: datetime) -> List[Order]:
        result: List[List[str]] = self.__sheets.values().get(
            spreadsheetId=self.__spreadsheet_id,
            range=self.__spreadsheet_range,
        ).execute().get('values', [])

        return sorted([
            Order(
                applicant_name=anonymize_name(row[1]),
                item_names=[item_name.strip().lower() for item_name in row[2:]]
            ) for row in result
            if row and datetime.strptime(row[0], '%d-%m-%Y %H:%M:%S') > min_datetime
        ])


def anonymize_name(name: str) -> str:
    parts = name.split(" ")
    result = parts[0]
    for part in parts[1:]:
        if part:
            result += " " + part[0]
    return result
