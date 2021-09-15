import datetime

from cachetools import cached, TTLCache
from flask import render_template

from models.dto import DTO
from repository import Repository


def process(_) -> str:
    global _repository
    data = _get_data()
    return render_template('frietlijst.html', dto=data)


def anonymize_name(name: str) -> str:
    parts = name.split(" ")
    result = parts[0]
    for part in parts[1:]:
        if part:
            result += " " + part[0]
    return result


@cached(cache=TTLCache(maxsize=2, ttl=10))
def _get_data() -> DTO:
    cutoff = datetime.datetime.now() - datetime.timedelta(days=4)

    rows_to_process = [row for row in _repository.load_rows()
                       if row and datetime.datetime.strptime(row[0], '%d-%m-%Y %H:%M:%S') > cutoff]

    result = DTO()

    for row in rows_to_process:
        result.add(
            applicant_name=anonymize_name(row[1]),
            item_names=[item_name.lower().strip() for item_name in row[2:]],
        )

    return result


if __name__ == 'main':
    _repository = Repository(
        sa_file_name='token.json',
        spreadsheet_id='18vCgc5DGUiFZN1NX_GBmxSBCb47KdsBkV6Glf9Sx-wE',
        spreadsheet_range='Friet bestelling!A2:F',
    )
