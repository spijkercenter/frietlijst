from typing import List


class Order:
    def __init__(self,
                 name: str,
                 items: List[str]):
        self.name = name
        self.items = items

    def __lt__(self: "Order",
               other: "Order"
               ) -> bool:
        return self.name < other.name
