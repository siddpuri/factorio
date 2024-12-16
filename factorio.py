from typing import Tuple, List, Dict

db_file_name = "recipes.txt"

class Item:
    name: str
    amount: int
    time: float
    ingredients: List[Tuple[str, int]]

    def __init__(self, name: str, amount: int, time: float):
        assert amount > 0
        assert time > 0
        self.name = name
        self.amount = amount
        self.time = time
        self.ingredients = []

    def __str__(self):
        return self.name

    def add(self, ingredient: Tuple[str, int]):
        self.ingredients.append(ingredient)

class Db:
    items: Dict[str, Item]

    def __init__(self):
        self.items = {}
        item = None
        with open(db_file_name) as f:
            for line in f:
                if not line.startswith(' '):
                    name, amount, time = line.split(", ")
                    assert self.items.get(name) is None
                    item = Item(name.strip(), int(amount), float(time))
                    self.items[name] = item
                else:
                    assert item is not None
                    name, amount = line.split(", ")
                    item.add(name.strip(), int(amount))
