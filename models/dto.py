from typing import List, Dict

from models.item import Item
from models.order import Order


class DTO:
    def __init__(self):
        self.__applicants: List[str] = []
        self.__items: Dict[str, int] = {}
        self.__orders: List[Order] = []

    def add(self, applicant_name: str, item_names: List[str]):
        self.__applicants.append(applicant_name)

        for item_name in item_names:
            if item_name not in self.__items:
                self.__items[item_name] = 0
            self.__items[item_name] += 1

        order = Order(applicant_name, item_names)
        self.__orders.append(order)

    @property
    def items(self) -> List[Item]:
        return sorted([Item(name, amount) for name, amount in self.__items.items()])

    @property
    def applicants(self) -> List[str]:
        return sorted(self.__applicants)

    @property
    def orders(self) -> List[Order]:
        return sorted(self.__orders)
