from typing import List, Dict, Optional, Set, Tuple, TypeVar
from collections import Counter, defaultdict
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


T = TypeVar("T")


def topological_sort(g: Dict[T, List[T]]) -> List[T]:
    result: List[T] = []

    all_nodes: Set[T] = set()
    nodes_with_permanent_mark: Set[T] = set()
    nodes_with_temporary_mark: Set[T] = set()

    for u in g:
        all_nodes.add(u)
        for v in g[u]:
            all_nodes.add(v)

    def visit(n: T):
        if n in nodes_with_permanent_mark:
            return
        if n in nodes_with_temporary_mark:
            raise ValueError("cycle in graph")

        nodes_with_temporary_mark.add(n)

        # for each node m with an edge from n to m do
        if n in g:
            for m in g[n]:
                visit(m)

        nodes_with_temporary_mark.remove(n)
        nodes_with_permanent_mark.add(n)
        result.insert(0, n)

    # while exists nodes without a permanent mark do
    while len(all_nodes - nodes_with_permanent_mark) > 0:
        # select an unmarked node n
        n = (all_nodes - nodes_with_permanent_mark).pop()
        visit(n)

    return result


class Reactions:
    @staticmethod
    def parse(text):
        # build dict of "output" as key and list of inputs needed to make that
        # output as the value
        ingredients: Dict[Item, List[Item]] = {}

        for line in text.strip().split("\n"):
            left, right = line.strip().split("=>")
            inputs = split_elements(left)
            output = split_element(right)

            ingredients[output] = inputs

        return Reactions(ingredients)

    def __init__(self, ingredients: Dict[Item, List[Item]]):
        # check that each output type appears once in the dict
        c = Counter([item.symbol for item in ingredients])
        assert set(c.values()) == {1}

        self.ingredients = ingredients

        # reverse the dict above, and store a normal representation of a graph, for use in topological sort
        g: Dict[str, List[str]] = defaultdict(list)
        for output, inputs in self.ingredients.items():
            for i in inputs:
                g[i.symbol].append(output.symbol)

        self.topological_sorted_nodes: List[str] = topological_sort(g)

    def topological_sort(self, items: List[Item]):
        """
        Topologically sort the list of items based on the graph of input symbols
        to output symbols. Assume items has a partial list of the symbol types
        present in the graph.
        """
        items = flatten(items)

        d = {item.symbol: item for item in items}

        return [d[symbol] for symbol in self.topological_sorted_nodes if symbol in d]

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
        # components holds the list of items we will be working on breaking down
        components = [Item(count, symbol)]

        # while there is still more items to break down, topologically sort the
        # list of components, and pop off the tail of the list and break that
        # down. merge results back into list, and continue, until the list has
        # only one item of ORE left.
        #
        # The intuition here is that by working on the tail item in the list, we
        # are always working with an item furthest down in the graph of
        # dependencies relative to others in the queue, and we'll only process
        # each symbol once, avoiding the problem where we might visit some
        # symbols too often and end up over counting because we had to round up
        # e.g. 3C to 5C because the recipe says 8A makes 5C. This causes a
        # problem if something we process later also produces C, and we'll
        # overcount if we don't realize we have that surplus of 2C.
        #
        # This code is a lot simpler than accounting for the problem described
        # above, compare this code to commit 66a6939e8.
        while len(components) > 1 or components[0].symbol != "ORE":
            # print(components)
            item = components.pop()
            inputs, output = self.get_inputs(item)
            # print(item, "->", inputs, f"(produces {output})")
            components.extend(inputs)

            # re-sort after extending the list, before checking the while loop's
            # conditions
            components = self.topological_sort(components)

        return components[0].num


def split_elements(line) -> List[Item]:
    """split a string like `1 A, 2 B, 3 C` into [Item(1, 'A'), Item(2, 'B'), Item(3, 'C')."""
    return [split_element(s) for s in line.split(",")]


def split_element(s) -> Item:
    """split a string like `1 A` into Item(1, 'A')."""
    e = s.strip().split(" ")
    assert len(e) == 2
    return Item(int(e[0]), e[1])
