from datetime import datetime, timedelta

from cachetools import cached, TTLCache
from flask import render_template, Flask

from item_service import ItemService
from order_repository import OrderRepository

app = Flask(__name__)
_repository = OrderRepository(
    sa_file_name='token.json',
    spreadsheet_id='18vCgc5DGUiFZN1NX_GBmxSBCb47KdsBkV6Glf9Sx-wE',
    spreadsheet_range='Friet bestelling!A2:F',
)

@app.route('/')
def process() -> str:
    return process_cached()


@cached(cache=TTLCache(maxsize=1, ttl=10))
def process_cached() -> str:
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
    app.run(debug==True)
