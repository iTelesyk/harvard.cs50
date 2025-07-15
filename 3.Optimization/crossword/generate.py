import sys

from crossword import *


class CrosswordCreator:

    def __init__(self, crossword: Crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            var_domain = self.domains[var]
            for word in set(var_domain):
                if len(word) != var.length:
                    var_domain.remove(word)

    def revise(self, x: Variable, y: Variable):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        # check do x and y even overlap
        overlaps = self.crossword.overlaps
        overlap_pos = overlaps[(x, y)]

        # return false if no overlap
        if overlap_pos is None:
            return revised

        x_domain = self.domains[x]
        y_domain = self.domains[y]
        for x_word in set(x_domain):
            x_satisfies_at_least_one_y = False
            x_char = x_word[overlap_pos[0]]
            for y_word in y_domain:
                y_char = y_word[overlap_pos[1]]
                if x_char == y_char:
                    x_satisfies_at_least_one_y = True
                    break  # break from y words loop
            if not x_satisfies_at_least_one_y:
                x_domain.remove(x_word)
                revised = True
        return revised

    def ac3(self, arcs=None) -> bool:
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = list()
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    arcs.append((x, y))

        queue = arcs.copy()
        while len(queue) > 0:
            arc = queue.pop()
            x, y = arc
            if self.revise(x, y):
                if self.domains[x] == 0:
                    return False
                else:
                    x_neighnors = self.crossword.neighbors(x).copy()
                    x_neighnors.remove(y)
                    for z in x_neighnors:
                        queue.append((z, x))

        for var in self.domains:
            if len(self.domains[var]) == 0:
                return False

        return True

    def assignment_complete(self, assignment: dict[Variable, str]):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # checks all variables in self.crossword.variables and makes sure that 
        # all of them have similar var in assignment and that word in not empty
        for var in self.crossword.variables:
            try:
                assigned_word = assignment[var]
                if assigned_word == "":
                    return False
            except KeyError:
                return False
        return True

    def consistent(self, assignment: dict[Variable, str]):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # checks for unary constrains
        for var, word in assignment.items():
            if var.length != len(word):
                return False

        # checks that all assigned words are unique
        words = list(assignment.values())
        unique_words = set(words)
        if len(words) != len(unique_words):
            return False

        # checks for binary constrains
        # for every word in assignment, compare it with other words in assignment
        # if they overlap, check that overlapping character is the same
        for x, x_word in assignment.items():
            for y, y_word in assignment.items():
                if x != y:
                    try:
                        overlap_pos = self.crossword.overlaps[(x, y)]
                    except KeyError:
                        return False
                    if overlap_pos is not None:
                        x_char = x_word[overlap_pos[0]]
                        y_char = y_word[overlap_pos[1]]
                        if x_char != y_char:
                            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # raise NotImplementedError
        return None

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # raise NotImplementedError
        return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        testing_ass = {
            Variable(0, 1, "down", 5): "SEVEN",
            Variable(4, 1, "across", 4): "NINE",
        }
        self.consistent(testing_ass)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
