import itertools
import random


class Minesweeper():
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


class Sentence():
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

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # 只有当self.cells元素个数等于count时才能判断mine
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # 只有当self.count=0时，所有cells是safe，其他情况无法判断
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

    def size(self):
        return len(self.cells)

    def equals(self, cells):
        return self.cells == cells


class MinesweeperAI():
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

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_mine_rest(self, source, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            if sentence is not source:
                sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def mark_safe_rest(self, source, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            if sentence is not source:
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
        # mark the cell as a move that has been made
        self.moves_made.add(cell)
        # mark the cell as safe
        self.mark_safe(cell)
        # add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`
        # 存储邻居位置
        neighbors = set()
        x, y = cell
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                x1 = x + i
                y1 = y + j
                # 合法的位置
                if self.height > x1 >= 0 and self.width > y1 >= 0:
                    # 未知
                    if (x1, y1) not in self.safes:
                        neighbors.add((x1, y1))
        next_sentence = Sentence(cells=neighbors, count=count)
        self.knowledge.append(next_sentence)
        for mine in self.mines:
            next_sentence.mark_mine(mine)

        continuing = True
        while continuing:
            # mark any additional cells as safe or as mines
            # if it can be concluded based on the AI's knowledge base
            continuing = False
            to_remove = []  # 删除已使用过的sentence
            for sentence in self.knowledge:
                s_mines = sentence.known_mines()
                # 如果能找出mines，只剩一个cell
                if len(s_mines) != 0:
                    to_remove.append(sentence)  # 待删除
                    for mine in s_mines:
                        self.mark_mine_rest(sentence, mine)
                    continuing = True
                    continue
                # 能找出safe的cells
                s_safes = sentence.known_safes()
                if len(s_safes) != 0:
                    to_remove.append(sentence)  # 待删除
                    for safe in s_safes:
                        self.mark_safe_rest(sentence, safe)
                    continuing = True
            self.knowledge = [x for x in self.knowledge if x not in to_remove]  # 删除已使用的sentence

            # add any new sentences to the AI's knowledge base
            # if they can be inferred from existing knowledge
            for sa in self.knowledge:
                for sb in self.knowledge:
                    if sa is not sb:
                        # 判断是否有子集关系
                        small, big = (sa, sb) if sa.size() < sb.size() else (sb, sa)
                        if small.cells.issubset(big.cells):
                            # 如果是子集，先检查knowledge中是否已经存在将要添加的sentence
                            dif = big.cells - small.cells
                            has_same = False
                            # 判断是否存在一样的
                            for sc in self.knowledge:
                                if sc.equals(dif):
                                    has_same = True
                                    break
                            if not has_same:
                                self.knowledge.append(Sentence(cells=dif, count=big.count - small.count))
                                continuing = True

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        possible_moves = self.safes - self.moves_made
        if len(possible_moves) == 0:
            return None
        return list(possible_moves)[0]

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.height):
            for j in range(self.width):
                move = (i, j)
                if move not in self.moves_made and move not in self.mines:
                    return move
        return None
