"""Name: Lauren Oliver, SID: 003100456"""

import re


class Boggle:

    SPECIAL_TILES = {"QU": 2, "ST": 2, "IE": 2}

    def __init__(self, grid, dictionary):
        """
        Constructor for Boggle class.

        Parameters:
        grid (list[list[str]]): 2D array representing the Boggle board.
        dictionary (list[str]): List of valid words.

        Initializes:
        self.solutions (set): Stores unique words found during search.
        """
        self.grid = grid
        self.dictionary = dictionary
        self.solutions = set()  # store unique words found

        if not self._grid_is_valid(self.grid):
            self.invalid_grid = True
        else:
            self.invalid_grid = False

    def setGrid(self, grid):
        """
        Setter method to update the game grid.

        Parameters:
        grid (2D array of strings): New NxN board of letters
        """
        self.grid = grid
        self.solutions = set()  # reset solutions when grid changes

    def setDictionary(self, dictionary):
        """
        Setter method to update the dictionary.

        Parameters:
        dictionary (list of strings): New list of valid words
        """
        self.dictionary = dictionary
        self.solutions = set()  # reset solutions when dictionary changes

    def getSolution(self):
        """
        Main solver method to find all valid words in the grid.

        Returns:
        list[str]: Sorted list of unique words found on the board.
        """
        # Ensure inputs exist
        if not self.grid or self.dictionary is None:
            return []

        size = len(self.grid)

        # Handle empty grid case
        if size == 0:
            return []

        # Grid must be square (NxN)
        if any(len(row) != size for row in self.grid):
            return []

        # Normalize everything to uppercase
        self.grid, self.dictionary = (
          self._normalize_input(self.grid, self.dictionary)
        )

        # Validate grid (all alphabetic tiles)
        if not self._grid_is_valid(self.grid):
            return []

        # Build prefix set + dictionary set for fast lookup
        word_set = set(self.dictionary)
        
        # Build prefix set - all prefixes of all words in dictionary for O(1) lookup
        prefix_set = set()
        for word in word_set:
            for i in range(1, len(word) + 1):
                prefix_set.add(word[:i])
        
        # Debug: Print some stats about the dictionary
        # print(f"Dictionary size: {len(word_set)}")
        # print(f"Prefix set size: {len(prefix_set)}")
        # print(f"Sample words: {list(word_set)[:10]}")
        # print(f"Words with length > 4: {sum(1 for w in word_set if len(w) > 4)}")

        visited = [[False] * size for _ in range(size)]

        # Explore from each grid position
        for r in range(size):
            for c in range(size):
                self._search("", r, c, visited, word_set, prefix_set, length=0)

        # return sorted(self.solutions)
        return sorted(word.upper() for word in self.solutions)

    def _normalize_input(self, grid, dictionary):
        """
        Convert grid letters and dictionary words to uppercase.
        Also filters dictionary to only include valid alphabetic words.

        Parameters:
        grid (list[list[str]]): Original grid.
        dictionary (list[str]): Original dictionary.

        Returns:
        tuple: (upper_grid, upper_dict)
        """
        upper_grid = [[cell.upper() for cell in row] for row in grid]
        # Filter dictionary to only include valid alphabetic words (no numbers, special chars, etc.)
        # Keep all words regardless of length - we want to find words of all lengths
        upper_dict = [word.upper() for word in dictionary if isinstance(word, str) and word.isalpha() and len(word) >= 2]
        return upper_grid, upper_dict

    def _grid_is_valid(self, grid):
        """
        Check that the grid contains only alphabetic strings.

        Parameters:
        grid (list[list[str]]): 2D Boggle board to validate.

        Returns:
        bool: True if all cells are strings and alphabetic, False otherwise.
        """
        for row in grid:
            for cell in row:
                if not isinstance(cell, str) or not cell.isalpha():
                    return False
                if cell.upper() == "Q":
                    return False
                if cell.upper() == "S":
                    return False
                if cell.upper() == "I":
                    return False
        return True

    def _is_prefix(self, prefix, prefix_set):
        """
        Check if the given prefix exists in the prefix set.
        Optimized from O(n) to O(1) lookup.

        Parameters:
        prefix (str): Current accumulated letters being evaluated during DFS.
        prefix_set (set[str]): Set of all prefixes of words in the dictionary.

        Returns:
        bool: True if prefix exists in the prefix set, False otherwise.
        """
        return prefix in prefix_set

    def _search(self, current, row, col, visited, wrd_set, prefix_set, length):
        """
        Perform depth-first search (DFS) from a given cell to find words.

        Parameters:
        current (str): Current accumulated word along DFS path.
        row (int): Row index of the current cell.
        col (int): Column index of the current cell.
        visited (list[list[bool]]): Tracks cells already used in current path.
        wrd_set (set[str]): Set of valid words.
        prefix_set (set[str]): Set of all prefixes of words in the dictionary.
        length (int): Accumulated word length accounting for special tiles.
        """
        n = len(self.grid)

        # Base case: stop if out of bounds or cell has already been visited
        if row < 0 or row >= n or col < 0 or col >= n or visited[row][col]:
            return

        # Retrieve current letter from the grid and add to current word
        # Convert tile to uppercase to keep consistent format
        tile = self.grid[row][col].upper()
        new_word = current + tile

        # Update word length with special tiles (count as multiple letters)
        new_length = length + self.SPECIAL_TILES.get(tile, 1)

        # Prune search early if no dictionary word begins with this prefix
        # O(1) lookup instead of O(n) - major performance improvement
        if not self._is_prefix(new_word, prefix_set):
            return

        # Mark this cell as visited to avoid reuse in the current path
        visited[row][col] = True

        # If valid word is found with length requirement, add to solutions
        # Note: We check both new_word and ensure it's in the word set
        # The word length check uses new_length (which accounts for special tiles)
        if new_word in wrd_set and new_length >= 3:
            self.solutions.add(new_word.upper())
        
        # IMPORTANT: Continue searching even after finding a word to find longer words
        # This allows us to find words like "ART" and "ARTS" from the same starting path
        # Explore all neighboring cells (8 directions)
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                self._search(
                    new_word,
                    row + dr,
                    col + dc,
                    visited,
                    wrd_set,
                    prefix_set,
                    new_length,
                )

        # Backtrack: unmark the cell so it can be used in other paths
        visited[row][col] = False  # backtrack


def main():
    grid = [
        ["T", "W", "Y", "R"],
        ["E", "N", "P", "H"],
        ["G", "Z", "Qu", "R"],
        ["O", "N", "T", "A"],
    ]
    dictionary = [
        "art",
        "ego",
        "gent",
        "get",
        "net",
        "new",
        "newt",
        "prat",
        "pry",
        "qua",
        "quart",
        "quartz",
        "rat",
        "tar",
        "tarp",
        "ten",
        "went",
        "wet",
        "arty",
        "rhr",
        "not",
        "quar",
    ]

    game = Boggle(grid, dictionary)
    print(game.getSolution())


if __name__ == "__main__":
    main()