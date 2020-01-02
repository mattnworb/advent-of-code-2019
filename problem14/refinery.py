from typing import List, Dict, Optional, Set, Tuple
from collections import Counter
from math import ceil
from functools import reduce


class Item:
    def __init__(self, num, symbol):
        self.num = num
        self.symbol = symbol

    def __eq__(self, value):
        return (
            isinstance(value, Item)
            and self.num == value.num
            and self.symbol == value.symbol
        )

    def __hash__(self):
        return hash((self.num, self.symbol))

    def __add__(self, value):
        assert isinstance(value, Item)
        assert self.symbol == value.symbol
        return Item(self.num + value.num, self.symbol)

    def __repr__(self):
        return f"{self.num} {self.symbol}"


def flatten(item_list: List[Item]) -> List[Item]:
    symbol_to_items: Dict[str, List[Item]] = {}

    for item in item_list:
        if item.symbol not in symbol_to_items:
            symbol_to_items[item.symbol] = [item]
        else:
            symbol_to_items[item.symbol].append(item)

    add = lambda a, b: Item(a.num + b.num, a.symbol)

    result: List[Item] = []
    for symbol, items in symbol_to_items.items():
        reduced = reduce(add, items)
        result.append(reduced)
    return result


class Reactions:
    @staticmethod
    def parse(text):
        ingredients = {}

        for line in text.strip().split("\n"):
            left, right = line.strip().split("=>")
            inputs = split_elements(left)
            output = split_element(right)

            ingredients[output] = inputs

        return Reactions(ingredients)

    def __init__(self, ingredients):
        # check that each output type appears once in the dict
        c = Counter([item.symbol for item in ingredients])
        assert set(c.values()) == {1}
        self.ingredients = ingredients

    def get_inputs(self, desired_item: Item) -> Tuple[List[Item], Item]:
        recipe_for_symbol: Optional[Item] = None
        for output, inputs in self.ingredients.items():
            if desired_item.symbol == output.symbol:
                assert recipe_for_symbol is None
                recipe_for_symbol = output

        assert (
            recipe_for_symbol is not None
        ), f"Could not find inputs that would turn into {desired_item}"

        # figure out how many multiples we need
        multiples = ceil(desired_item.num / recipe_for_symbol.num)
        return (
            self.multiply_items(multiples, self.ingredients[recipe_for_symbol]),
            Item(multiples * recipe_for_symbol.num, recipe_for_symbol.symbol),
        )

    def multiply_items(self, count: int, items: List[Item]):
        return [Item(count * i.num, i.symbol) for i in items]

    def calculate_ore(self, count: int, symbol: str):
        components = [Item(count, symbol)]

        while True:
            print("Components:", components)
            new_list: List[Item] = []
            broke_something_down = False
            for item in components:
                if item.num < 0:
                    # recording a credit - leave alone
                    new_list.append(item)
                    continue
                inputs, output = self.get_inputs(item)
                # keep this in the list, don't transform to ORE
                if len(inputs) == 1 and inputs[0].symbol == "ORE":
                    print(f"Not breaking down {item} because {inputs[0]} => {output}")
                    new_list.append(item)
                else:
                    print(item, "=>", inputs, "=>", output)
                    new_list.extend(inputs)
                    broke_something_down = True

                    # Lets say the item was `3 C` and the matchine reaction was
                    # something like `10B => 5C`. Since we had to round up to go
                    # backwards from C to B, we have 2C "left over". Record this
                    # as a negative count item in case we later need to break
                    # down a `C`. Without doing this, we might come across an
                    # item like `2 C`, which if we had waited to turn C into B
                    # until we had "all" the C, we could convert cleanly into
                    # 10B. Without recording the "credit", we would round up 3 C
                    # to 5 C and get 10 B and round up 2 C to 5 C and get
                    # another 10 B for a total of 20 B - when the optimal move
                    # was to turn (3 C + 2C) = 5 C into just 10 B.
                    #
                    # A better overall algorithm here would be to topologically
                    # sort the list of components on each list iteration, and
                    # break down the tail item repeatedly until the list had
                    # only one item of ORE left.
                    if output.num > item.num:
                        diff = item.num - output.num
                        credit = Item(diff, item.symbol)
                        new_list.append(credit)
                        print(f"left over: {diff} {item.symbol}")

            flattened = flatten(new_list)
            print(components, "became", new_list, "which flattens to", flattened, "\n")
            components = flattened

            if not broke_something_down:
                print("stopping because nothing was broken down")
                break

        # at this point, list cannot be broken down any further .. turn it into ORE
        print("reduced components to", components)
        ore_needed = 0
        for item in components:
            if item.num < 0:
                continue
            inputs, output = self.get_inputs(item)
            assert len(inputs) == 1 and inputs[0].symbol == "ORE"
            print(item, "=>", inputs[0])
            ore_needed += inputs[0].num

        return ore_needed


def split_elements(line):
    """split a string like `1 A, 2 B, 3 C` into [Item(1, 'A'), Item(2, 'B'), Item(3, 'C')."""
    return [split_element(s) for s in line.split(",")]


def split_element(s):
    """split a string like `1 A` into Item(1, 'A')."""
    e = s.strip().split(" ")
    assert len(e) == 2
    return Item(int(e[0]), e[1])
