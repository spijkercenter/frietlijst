from typing import List, Dict

from item_builder import ItemBuilder
from models.item import Item
from models.order import Order


class OrderTotal:
    def __init__(self):
        self.__orders: List[Order] = []

    def add(self, order: Order) -> None:
        self.__orders.append(order)

    @property
    def items(self) -> List[Item]:
        return ItemBuilder(self.__orders).build()

    @property
    def item_count(self) -> int:
        return sum([len(o.items) for o in self.__orders])

    @property
    def applicants(self) -> List[str]:
        return sorted([o.name for o in self.__orders])

    @property
    def orders(self) -> List[Order]:
        return sorted(self.__orders)
