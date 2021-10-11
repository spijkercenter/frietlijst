import re
from typing import List, Dict

import Levenshtein

from models.item import Item
from models.order import Order


class ItemService:
    @staticmethod
    def _translate_part(item_names: List[str], old: str, new: str) -> List[str]:
        return [i.replace(old, new) for i in item_names]

    @staticmethod
    def _translate_part_regex(item_names: List[str], regex: str, new: str) -> List[str]:
        return [re.sub(regex, new, i) for i in item_names]

    @staticmethod
    def _translate_whole(item_names: List[str], old: str, new: str) -> List[str]:
        return [new if i == old else i for i in item_names]

    @staticmethod
    def _consolidate_names(item_names: List[str]) -> List[str]:
        uq_item_names: List[str] = list(set(item_names))
        print(uq_item_names)
        for idx, lhs in enumerate(uq_item_names):
            for rhs in uq_item_names[idx + 1:]:
                if lhs[0:2] == rhs[0:2]:
                    distance = Levenshtein.distance(lhs, rhs)
                    if distance <= 2:
                        print(lhs + ":" + rhs + " = " + str(distance))
                        item_names = ItemService._translate_whole(item_names, lhs, rhs)
        return item_names

    @staticmethod
    def _aggregate_items(item_names: List[str]) -> List[Item]:
        items: Dict[str, int] = {}
        for item_name in item_names:
            if item_name not in items:
                items[item_name] = 0
            items[item_name] += 1
        return sorted([Item(n, a) for n, a in items.items()])

    @staticmethod
    def get_items_from_orders(orders: List[Order]):
        item_names: List[str] = _flatten([o.items for o in orders])
        item_names = ItemService._translate_part_regex(item_names, r" ?\+ ?", " + ")
        item_names = ItemService._translate_part_regex(item_names, r" met$", " met mayo")
        item_names = ItemService._translate_part_regex(item_names, r" (mayo[^ ]*)", " mayo")
        item_names = ItemService._translate_part_regex(item_names, r" sat[eé](saus)?", " saté")
        item_names = ItemService._translate_part(item_names, "patat", "friet")
        item_names = ItemService._translate_part(item_names, "frietje", "friet")
        item_names = ItemService._translate_part(item_names, "krul friet", "twister")
        item_names = ItemService._translate_part(item_names, "krulfriet", "twister")

        item_names = ItemService._consolidate_names(item_names)

        return sorted(ItemService._aggregate_items(item_names))


def _flatten(t: List[List]) -> List:
    return [item for sublist in t for item in sublist]
