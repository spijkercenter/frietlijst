from typing import List


class Order:
    def __init__(self,
                 applicant_name: str,
                 item_names: List[str]):
        self.name = applicant_name
        self.items = item_names

    def __lt__(self: "Order",
               other: "Order"
               ) -> bool:
        return self.name < other.name
