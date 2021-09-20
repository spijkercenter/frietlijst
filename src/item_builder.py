from typing import List, Dict

import Levenshtein

from models.item import Item
from models.order import Order


class ItemBuilder:
    def __init__(self, orders: List[Order]):
        self.__item_names: List[str] = _flatten([o.items for o in orders])

    def _translate_part(self, old: str, new: str) -> None:
        self.__item_names = [i.replace(old, new) for i in self.__item_names]

    def _translate_whole(self, old: str, new: str) -> None:
        self.__item_names = [new if i == old else i for i in self.__item_names]

    def _consolidate_names(self) -> None:
        uq_item_names: List[str] = list(set(self.__item_names))
        print(uq_item_names)
        for idx, lhs in enumerate(uq_item_names):
            for rhs in uq_item_names[idx + 1:]:
                if lhs[0:2] == rhs[0:2]:
                    distance = Levenshtein.distance(lhs, rhs)
                    if distance <= 2:
                        print(lhs + ":" + rhs + " = " + str(distance))
                        self._translate_whole(lhs, rhs)

    def _aggregate_names(self) -> List[Item]:
        items: Dict[str, int] = {}
        for item_name in self.__item_names:
            if item_name not in items:
                items[item_name] = 0
            items[item_name] += 1
        return sorted([Item(n, a) for n, a in items.items()])

    def build(self) -> List[Item]:
        self._translate_part("frietje", "friet")
        self._translate_part("krul friet", "twister")
        self._translate_part("krulfriet", "twister")

        self._consolidate_names()

        return self._aggregate_names()


def _flatten(t: List[List]) -> List:
    return [item for sublist in t for item in sublist]
