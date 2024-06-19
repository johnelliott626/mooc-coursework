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
        for variable, domain in self.domains.items():
            words = domain.copy()
            for word in words:
                if len(word) != variable.length:
                    domain.remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Check if the x and y overlap on the crossword puzzle.
        does_overlap = self.crossword.overlaps[x, y]
        if does_overlap:
            x_overlap_char, y_overlap_char = does_overlap

            # Remove values from X's domain that does not have a possible corresponding values in Y
            x_domain = self.domains[x].copy()
            y_domain = self.domains[y]
            revision_made = False

            for x_word in x_domain:
                is_x_word_valid_in_y_domain = False
                for y_word in y_domain:
                    if x_word[x_overlap_char] == y_word[y_overlap_char]:
                        is_x_word_valid_in_y_domain = True
                        break
                if not is_x_word_valid_in_y_domain:
                    self.domains[x].remove(x_word)
                    revision_made = True
            return revision_made
        else:
            return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
       
        # Generate a list of arcs
        if arcs is not None:
            queue = arcs
        else:
            queue = []
            variables = self.crossword.variables
            for x in variables:
                for y in variables:
                    if x != y and self.crossword.overlaps[x, y]:
                        queue.append((x, y))
        
        # Enforce arc consistency with the ac3 algorithm
        while queue:
            x, y = queue.pop(0)

            # If a revision needs to be made in the arc
            if self.revise(x, y):
                # Return false if the domain for x is empty
                if len(self.domains[x]) == 0:
                    return False
                
                # A revision was made, so enqueue each neighbor arc from neighbor to x
                for neighbor in self.crossword.neighbors(x):
                    queue.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return True if len(assignment) == len(self.crossword.variables) else False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        # Check unary constraints
        # Distinct values
        if len(assignment.values()) != len(set(assignment.values())):
            return False
        # Correct length
        for variable, word in assignment.items():
            if len(word) != variable.length:
                return False
        
        # Check binary constraints
        for variable, word in assignment.items():
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    overlap_indicies = self.crossword.overlaps[variable, neighbor]
                    if overlap_indicies:
                        word_overlap_char, neighbor_overlap_char = overlap_indicies
                        if word[word_overlap_char] != assignment[neighbor][neighbor_overlap_char]:
                            return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # The unordered domain values for var
        original_domain = self.domains[var]

        # Elimination map to count the number of neighbor variable eliminations for each word in the original domain
        elimination_map = { word : 0 for word in original_domain }

        # Compute number of eliminations for each word in the domain
        for word in original_domain:
            for neighbor in self.crossword.neighbors(var):
                # If a neighbor is already in the assignment it already has an assigned value, so skip it
                if neighbor not in assignment:
                    # Overlapping character indices
                    var_overlap_index, neighbor_overlap_index = self.crossword.overlaps[var, neighbor]
                    word_overlap_char = word[var_overlap_index]

                    # Increment elimination map count if the word eliminates a word from the neighbors domain
                    neighbor_domain = self.domains[neighbor]
                    for neighbor_word in neighbor_domain:
                        if neighbor_word[neighbor_overlap_index] != word_overlap_char:
                            elimination_map[word] += 1

        # Sort the domain in ascending order of the elimination map
        ordered_domain = sorted(elimination_map, key=lambda word: elimination_map[word])
        return ordered_domain

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        all_variables = self.crossword.variables
        unassigned_variables = [var for var in all_variables if var not in assignment]

        # Count domain and degree of each unassigned variable
        domain_degree_map = dict()
        for var in unassigned_variables:
            num_words = len(self.domains[var])
            num_degrees = len(self.crossword.neighbors(var))
            domain_degree_map[var] = (num_words, num_degrees)
        
        # Return the variable with the minimum number of remaining values in its domain, break ties with highest degree
        select_variable = min(domain_degree_map, key=lambda var: (domain_degree_map[var][0], -domain_degree_map[var][1]))
        return select_variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Base case: check if assignment is a solution
        if self.assignment_complete(assignment) and self.consistent(assignment):
            return assignment

        # Select next unassigned variable
        variable = self.select_unassigned_variable(assignment)

        # Order domain values of the selected variable
        ordered_domain = self.order_domain_values(variable, assignment)

        # Iterate through the ordered domain values
        for word in ordered_domain:
            # Create a new assignment
            new_assignment = assignment.copy()
            new_assignment[variable] = word

            # Check if the new assignment is consistent
            if self.consistent(new_assignment):
                # Recursively call backtrack with the new assignment
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
                
        # Return none if no solution was found (backtrack)
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
