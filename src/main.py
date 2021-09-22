from datetime import datetime, timedelta

from flask import render_template

from item_service import ItemService
from order_repository import OrderRepository


def process(_) -> str:
    min_datetime = datetime.now() - timedelta(days=2)
    orders = _repository.find_by_datetime_placed_greater_than(min_datetime)

    items = ItemService.get_items_from_orders(orders)
    item_count = sum([len(o.items) for o in orders])
    applicants = [o.name for o in orders]

    return render_template('frietlijst.html',
                           applicants=applicants,
                           items=items,
                           item_count=item_count,
                           orders=orders,
                           )


if __name__ == 'main':
    _repository = OrderRepository(
        sa_file_name='token.json',
        spreadsheet_id='18vCgc5DGUiFZN1NX_GBmxSBCb47KdsBkV6Glf9Sx-wE',
        spreadsheet_range='Friet bestelling!A2:F',
    )
