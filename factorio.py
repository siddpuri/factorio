from typing import Tuple, List, Dict, Set

db_file_name = "recipes.txt"

speeds = {
    "Raw": 1,
    "Furnace": 2,
    "Factory": 0.75,
    "Chemical plant": 1,
}

targets = [
    "Red science",
    "Green science",
    "Gray science",
    "Blue science",
    "Purple science",
]

rate = 0.3

class Item:
    name: str
    amount: int
    time: float
    sequence: int
    ingredients: List[Tuple["Item", int]]

    def __init__(self, name: str, amount: int, time: float, sequence: int):
        self.name = name
        self.amount = amount
        self.time = time
        self.sequence = sequence
        self.ingredients = []

    def __str__(self):
        return self.name

    def add(self, ingredient: "Item", amount: int):
        self.ingredients.append((ingredient, amount))

class Catalog:
    items: Dict[str, Item]

    def __init__(self):
        self.items = {}
        self.read_recipes()

    def read_recipes(self) -> None:
        speed = 1
        item = None
        with open(db_file_name) as f:
            for line in f:
                indented = line.startswith(" ")
                line = line.strip()
                if not line:
                    pass
                elif line.startswith("["):
                    speed = speeds[line[1:-1]]
                elif not indented:
                    if ", " in line:
                        name, amount, time = line.split(",")
                    else:
                        name, amount, time = line, 1, 1
                    assert name not in self.items
                    item = Item(name, int(amount), float(time) / speed, len(self.items))
                    self.items[name] = item
                else:
                    name, amount = line.split(", ")
                    item.add(self.items[name], int(amount))

class ShoppingList:
    items: List[Item]
    rates: List[float]

    def __init__(self, item: Item, rate: float):
        self.items = []
        self.add_ingredients(item)
        self.items.sort(key=lambda x: x.sequence, reverse=True)
        self.calculate_rates(rate)

    def add_ingredients(self, item: Item) -> None:
        if item in self.items:
            return
        self.items.append(item)
        for ingredient, _ in item.ingredients:
            self.add_ingredients(ingredient)

    def calculate_rates(self, rate) -> None:
        self.rates = [0] * len(self.items)
        self.rates[0] = rate
        for i in range(len(self.items)):
            for ingredient, amount in self.items[i].ingredients:
                j = self.items.index(ingredient)
                assert j > i
                self.rates[j] += self.rates[i] / self.items[i].amount * amount

    def print(self) -> None:
        for i in range(len(self.items)):
            if not self.items[i].ingredients:
                continue
            item = self.items[i]
            rate = self.rates[i]
            print(f"{item.name:16}: {rate:4.1f} {rate * item.time / item.amount:4.1f}")
        print()

class Toplevel:
    db: Catalog

    def __init__(self):
        self.db = Catalog()

    def repl(self) -> None:
        while True:
            name = input("Enter item name: ")
            if not name:
                return
            item = self.db.items.get(name)
            if item is None:
                print(f"Item {name} not found")
            else:
                ShoppingList(item, rate).print()

    def batch(self) -> None:
        for target in targets:
            item = self.db.items[target]
            print(target)
            print("=" * len(target))
            ShoppingList(item, rate).print()

Toplevel().batch()
