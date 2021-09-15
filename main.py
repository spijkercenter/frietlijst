import datetime
from typing import List

from flask import render_template
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from models.dto import DTO

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


def _anonymize_name(name: str) -> str:
    parts = name.split(" ")
    result = parts[0]
    for part in parts[1:]:
        if part:
            result += " " + part[0]
    return result


def _load_values() -> List[List[str]]:
    credentials: Credentials = Credentials.from_service_account_file('token.json', scopes=_SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    sheets = service.spreadsheets()
    result = sheets.values().get(spreadsheetId=_SHEET_ID, range=_RANGE).execute()
    values = result.get('values', [])
    return values


def _get_data() -> DTO:
    cutoff = datetime.datetime.now() - datetime.timedelta(days=4)

    rows_to_process = [row for row in _load_values()
                       if row and datetime.datetime.strptime(row[0], '%d-%m-%Y %H:%M:%S') > cutoff]

    result = DTO()

    for row in rows_to_process:
        result.add(
            applicant_name=_anonymize_name(row[1]),
            item_names=[item_name.lower().strip() for item_name in row[2:]],
        )

    return result
