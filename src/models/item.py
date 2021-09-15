class Item:
    def __init__(self,
                 name: str,
                 amount: int):
        assert name == name.lower()
        self.name = name
        self.amount = amount
        self.__contains_fries = 'friet' in self.name or 'twister' in self.name

    def __lt__(self: "Item",
               other: "Item"
               ) -> bool:
        if self.__contains_fries and not other.__contains_fries:
            return True
        if not self.__contains_fries and other.__contains_fries:
            return False
        return self.name < other.name
