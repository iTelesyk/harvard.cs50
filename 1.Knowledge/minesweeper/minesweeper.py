import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self) -> set[tuple]:
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self) -> set[tuple]:
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0 and len(self.cells) > 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        else:
            pass

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            pass


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        self.blanc_cells = self._populate_blancs()

        # List of sentences about the game known to be true
        self.knowledge = []

    def _populate_blancs(self) -> set[tuple]:
        cells = set()
        for i in range(self.height):
            for j in range(self.width):
                cells.add((i, j))
        return cells

    def _clean_knowledge(self):
        for s in list(self.knowledge):
            if s.count > len(s.cells):
                raise ValueError
            if len(s.cells) == 0:
                self.knowledge.remove(s)

    def _print_knowledge(self):
        
        print(f"Moves made: {len(self.moves_made)}")
        print(f"Safe moves: {self.safes}")
        print(f"Known mines: {self.mines}")
        print(f"Current knowledge base:")
        for s in self.knowledge:
            print(s)

    def _add_sentence_to_knowledge(self, new_sentence: Sentence):
        if not (new_sentence in self.knowledge):
            self.knowledge.append(new_sentence)

    def list_nearby_cells(self, cell) -> set:
        nearby_cells = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    nearby_cells.add((i, j))
        return nearby_cells

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as a move
        # self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`
        nearby_cells = self.list_nearby_cells(cell)

        know_mines_and_safes = self.mines | self.safes
        cell_to_consider = nearby_cells.difference(know_mines_and_safes)

        if len(cell_to_consider) > 0:
            new_sentence = Sentence(cells=cell_to_consider, count=count)
            self._add_sentence_to_knowledge(new_sentence)
            print(f"Added new sentence: {new_sentence}")

        # 4) mark any additional cells as safe or as mines
        # if it can be concluded based on the AI's knowledge base
        is_knowlendge_changed = True
        while is_knowlendge_changed:
            is_knowlendge_changed = False
            self._clean_knowledge()

            self._print_knowledge()
            for sentence in self.knowledge:
                know_safes = sentence.known_safes()
                for cell in set(know_safes):
                    if cell not in self.safes:
                        self.mark_safe(cell)
                        is_knowlendge_changed = True
                know_mines = sentence.known_mines()
                for cell in set(know_mines):
                    if cell not in self.mines:
                        self.mark_mine(cell)
                        is_knowlendge_changed = True

            # 5) draw conclusions from
            # if sentence is 1 cell long, than we solved it
            for sentence in list(self.knowledge):
                if len(sentence.cells) == 1:
                    only_cell = next(iter(sentence.cells))
                    if sentence.count == 0:
                        self.mark_safe(only_cell)
                    if sentence.count == 1:
                        self.mark_mine(only_cell)

            for s in list(self.knowledge):
                for other_s in list(self.knowledge):
                    if s != other_s and len(other_s.cells) != 0 and len(s.cells) != 0:
                        s_cells = s.cells
                        s_count = s.count
                        other_cells = other_s.cells
                        other_count = other_s.count
                        if other_cells.issubset(s_cells):
                            print(f"Set: {s}")
                            print(f"Subset: {other_s}")
                            deducted_sentence = Sentence(
                                s_cells - other_cells, s_count - other_count
                            )
                            print(f"Deducted sentence: {deducted_sentence}")
                            self._add_sentence_to_knowledge(deducted_sentence)
                            # TODO: line below causes infinite loop
                            is_knowlendge_changed = True

    def make_safe_move(self) -> tuple:
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) > 0:
            # Calculate the union of moves_made and mines
            explored_or_mined = self.moves_made.union(self.mines)
            # Find elements in safes that are not in explored_or_mined
            available_safes = self.safes.difference(explored_or_mined)
            # If there are any such elements, pick one (e.g., the first one)
            if available_safes:
                chosen_move = next(iter(available_safes))
                print(f"I pick this safe cell: {chosen_move}")
                return chosen_move
            else:
                return None
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Remove cells that have already been played, flagged as mines, or safe
        unavailable = self.moves_made | self.mines | self.safes
        # Remove all unavailable cells from blanc_cells
        self.blanc_cells = self.blanc_cells.difference(unavailable)

        random_cell = random.choice(list(self.blanc_cells))
        print(f"Picked a random cell {random_cell}")
        return random_cell
