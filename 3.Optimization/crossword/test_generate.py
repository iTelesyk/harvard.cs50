import pytest
from crossword import Crossword, Variable
from generate import CrosswordCreator

# Mock data from structure0.txt and words0.txt
structure = [
    [True, False, False, False, True],
    [True, False, True, True, False],
    [True, False, True, True, False],
    [True, False, True, True, False],
    [True, True, True, True, True]
]
words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

class MockCrossword(Crossword):
    def __init__(self):
        self.structure = structure
        self.words = words
        # Create two variables that overlap at one position
        self.variables = set()
        # Variable 1: ACROSS at (0,0), length 3
        self.var1 = Variable(0, 0, "ACROSS", 3)
        # Variable 2: DOWN at (0,2), length 5
        self.var2 = Variable(0, 2, "DOWN", 5)
        self.variables.add(self.var1)
        self.variables.add(self.var2)
        # Overlap at (0,2): var1[2] and var2[0]
        self.overlaps = {
            (self.var1, self.var2): (2, 0),
        }

    def neighbors(self, var):
        return {v for v in self.variables if v != var}

    def overlap(self, x, y):
        return self.overlaps.get((x, y), None)

def test_revise_no_overlap():
    # Setup crossword with two variables that do NOT overlap
    cw = MockCrossword()
    creator = CrosswordCreator(cw)
    # Add a third variable that does not overlap
    var3 = Variable(4, 4, "ACROSS", 3)
    cw.variables.add(var3)
    creator.domains[var3] = ["one", "two", "six"]
    result = creator.revise(cw.var1, var3)
    assert result is False
    assert set(creator.domains[cw.var1]) == set(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"])


def test_revise_overlap_no_removal():
    # Setup crossword with overlap, all x values have a match in y
    cw = MockCrossword()
    creator = CrosswordCreator(cw)
    # Set domains so all x words match y words at overlap
    creator.domains[cw.var1] = ["one"]  # 'one'[2] == 'e'
    creator.domains[cw.var2] = ["eight", "eleven"]  # both start with 'e'
    result = creator.revise(cw.var1, cw.var2)
    assert result is False
    assert creator.domains[cw.var1] == ["one"]


def test_revise_overlap_removal():
    # Setup crossword with overlap, some x values do not match y
    cw = MockCrossword()
    creator = CrosswordCreator(cw)
    creator.domains[cw.var1] = ["one", "two", "six"]  # 'one'[2]='e', 'two'[2]='o', 'six'[2]='x'
    creator.domains[cw.var2] = ["eight", "eleven"]  # both start with 'e'
    result = creator.revise(cw.var1, cw.var2)
    # Only 'one' should remain
    assert result is True
    assert creator.domains[cw.var1] == ["one"]


def test_revise_overlap_all_removed():
    # Setup crossword with overlap, all x values removed
    cw = MockCrossword()
    creator = CrosswordCreator(cw)
    creator.domains[cw.var1] = ["two", "six"]  # 'two'[2]='o', 'six'[2]='x'
    creator.domains[cw.var2] = ["eight", "eleven"]  # both start with 'e'
    result = creator.revise(cw.var1, cw.var2)
    assert result is True
    assert creator.domains[cw.var1] == []


