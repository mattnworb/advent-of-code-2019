from .refinery import Reactions, split_elements, Item, topological_sort

import pytest  # type: ignore


def test_topological_sort():
    g = {"a": ["b", "c"], "b": ["d", "e"], "d": ["f"]}

    ts = topological_sort(g)
    # don't need to assert length, below code implicity asserts each node in
    # the graph is in the list.

    # "a topological sort or topological ordering of a directed graph is a
    # linear ordering of its vertices such that for every directed edge uv from
    # vertex u to vertex v, u comes before v in the ordering"
    for u in g:
        for v in g[u]:
            u_pos = ts.index(u)
            v_pos = ts.index(v)
            assert u_pos < v_pos


def test_topological_sort_with_cycle():
    # same as above but with a connection from d -> a
    g = {"a": ["b", "c"], "b": ["d", "e"], "d": ["f", "a"]}

    with pytest.raises(ValueError) as excinfo:
        ts = topological_sort(g)
    excinfo.match("cycle in graph")


class TestItem:
    def test_eq(self):
        assert Item(5, "A") == Item(5, "A")
        assert Item(1, "A") != Item(5, "A")


def test_split_elements():
    x = "2 AB, 3 BC, 4 CA"
    assert [Item(2, "AB"), Item(3, "BC"), Item(4, "CA")] == split_elements(x)


EXAMPLE_1 = """
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""

EXAMPLE_2 = """
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
"""

EXAMPLE_3 = """
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""

EXAMPLE_4 = """
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
"""

EXAMPLE_5 = """
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"""

EXAMPLE_X = """
2 ORE => 2 A
3 ORE => 2 B
5 ORE => 5 D
1 A, 2 B => 2 C
12 A, 4 B => 2 AB
1 A, 2 B, 3 C, 9 D, 1 AB => 1 FUEL
"""

# 1 A, 2 B, 3 C, 9 D, (1 AB)
# 1 A, 2 B, 3 C, 9 D, 12 A, 4 B
# 13 A, 6 B, (3 C), 9 D
# 13 A, 6 B, 2 A, 4 B, 9 D
# 15 A, 10 B, 9 D
# 16, 15, 19 = 41

SIMPLE_BUG_REPRO = """
3 a, 1 b, 2 c => 1 FUEL
1 ORE => 1 a
3 a => 2 b
1 b => 2 c
"""


class TestReactions:
    def test_parse(self):
        r = Reactions.parse(
            """
            10 ORE => 5 A
            3 ORE => 2 B
        """
        )
        assert r.ingredients[Item(5, "A")] == [Item(10, "ORE")]
        assert r.ingredients[Item(2, "B")] == [Item(3, "ORE")]

    def test_get_inputs(self):
        r = Reactions.parse(
            """
            10 ORE => 5 A
            3 ORE => 2 B
            12 A, 4 B => 2 C
        """
        )

        assert r.get_inputs(Item(6, "B")) == ([Item(9, "ORE")], Item(6, "B"))
        assert r.get_inputs(Item(1, "A")) == ([Item(10, "ORE")], Item(5, "A"))
        assert r.get_inputs(Item(4, "A")) == ([Item(10, "ORE")], Item(5, "A"))

        assert r.get_inputs(Item(2, "C")) == (
            [Item(12, "A"), Item(4, "B")],
            Item(2, "C"),
        )
        assert r.get_inputs(Item(3, "C")) == (
            [Item(24, "A"), Item(8, "B")],
            Item(4, "C"),
        )
        assert r.get_inputs(Item(4, "C")) == (
            [Item(24, "A"), Item(8, "B")],
            Item(4, "C"),
        )

    @pytest.mark.parametrize(
        "recipe,expected",
        [
            (EXAMPLE_1, 31),
            (EXAMPLE_2, 165),
            (EXAMPLE_3, 13312),
            (EXAMPLE_4, 180697),
            (EXAMPLE_5, 2210736),
            (EXAMPLE_X, 41),
            (SIMPLE_BUG_REPRO, 6),
        ],
        ids=[
            "EXAMPLE_1",
            "EXAMPLE_2",
            "EXAMPLE_3",
            "EXAMPLE_4",
            "EXAMPLE_5",
            "EXAMPLE_X",
            "SIMPLE_BUG_REPRO",
        ],
    )
    def test_calculate_ore(self, recipe, expected):
        r = Reactions.parse(recipe)
        assert expected == r.calculate_ore(1, "FUEL")
