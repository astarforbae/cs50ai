import random
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
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
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
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
        # 遍历每个Variable
        for var in self.domains:
            var_domain = self.domains[var].copy()
            for available_value in self.domains[var]:
                if len(available_value) != var.length:
                    var_domain.remove(available_value)
            self.domains[var] = var_domain

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # 获得重叠位置
        # 遍历x的domain，删除那些无法在y中找到相对应值的
        i, j = self.crossword.overlaps[x, y]
        new_domain_of_x = self.domains[x].copy()
        changes_made_on_domain = False
        for available_value in self.domains[x]:
            x_on_shared = available_value[i]
            has_corresponding = False
            for y_available_value in self.domains[y]:
                y_on_shared = y_available_value[j]
                if x_on_shared == y_on_shared:
                    has_corresponding = True
                    break
            if not has_corresponding:
                new_domain_of_x.remove(available_value)
                changes_made_on_domain = True
        if changes_made_on_domain:
            self.domains[x] = new_domain_of_x

        return changes_made_on_domain

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # 创建队列
        ac3_queue = []  # 列表模拟队列
        if arcs is None:
            for x in self.domains:
                for y in self.crossword.neighbors(x):
                    ac3_queue.append((x, y))
        else:
            ac3_queue = arcs.copy()
        while len(ac3_queue) != 0:
            x, y = ac3_queue[0]
            ac3_queue = ac3_queue[1:]
            if self.revise(x, y):
                # 如果发生过修改
                if len(self.domains[x]) == 0:
                    return False
                for x_neighbor in self.crossword.neighbors(x):
                    ac3_queue.append((x_neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            if var not in assignment or assignment[var] is None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        check_distinct_set = set()
        for var in assignment:
            assigned_word = assignment[var]

            # 检查唯一
            if assigned_word in check_distinct_set:
                return False
            # 检查长度
            if len(assigned_word) != var.length:
                return False

            check_distinct_set.add(var)

        for var in assignment:
            neighbors = self.crossword.neighbors(var)
            for neighbor in assignment:
                if neighbor in neighbors:
                    x, y = self.crossword.overlaps[var, neighbor]
                    if assignment[var][x] != assignment[neighbor][y]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        available_values = [key for key in self.domains[var]]
        counters = [0 for x in available_values]
        for i in range(len(available_values)):
            value = available_values[i]
            counter = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    continue
                x, y = self.crossword.overlaps[var, neighbor]
                for neighbor_value in self.domains[neighbor]:
                    if value[x] != neighbor_value[y]:
                        counter += 1
            counters[i] = counter
        ans = [(available_values[i], counters[i]) for i in range(len(available_values))]
        return [x for (x, _) in sorted(ans, key=lambda pair: pair[1])]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        undetermined = set(self.domains) - set(assignment)
        # 选择可选值最少的
        least_available_value_count = None
        for var in undetermined:
            available_value_count = len(self.domains[var])
            if least_available_value_count is None:
                least_available_value_count = available_value_count
            elif available_value_count < least_available_value_count:
                least_available_value_count = available_value_count
        available_vars = []
        for var in undetermined:
            available_value_count = len(self.domains[var])
            if available_value_count == least_available_value_count:
                available_vars.append(var)
        if len(available_vars) == 1:
            return available_vars[0]

        # 选择度数大的
        var_neighbor = {}
        most_neighbor_count = None
        for var in available_vars:
            neighbor_count = len(self.crossword.neighbors(var))
            var_neighbor[var] = neighbor_count
            if most_neighbor_count is None:
                most_neighbor_count = neighbor_count
            elif neighbor_count > most_neighbor_count:
                most_neighbor_count = neighbor_count
        available_vars = [x for x in available_vars if var_neighbor[x] == most_neighbor_count]
        return random.choice(available_vars)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                self.backtrack(assignment)
                if self.assignment_complete(assignment):
                    return assignment
            del assignment[var]

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
