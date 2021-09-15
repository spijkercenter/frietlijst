from typing import List

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class Repository:
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

    def load_rows(self) -> List[List[str]]:
        result = self.__sheets.values().get(
            spreadsheetId=self.__spreadsheet_id,
            range=self.__spreadsheet_range,
        ).execute()
        return result.get('values', [])
