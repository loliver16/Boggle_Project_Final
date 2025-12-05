/**
 * Boggle Solver - JavaScript implementation
 * Based on the Python boggle_solver.py logic
 */

class BoggleSolver {
  static SPECIAL_TILES = { "QU": 2, "ST": 2, "IE": 2 };

  constructor(grid, dictionary) {
    this.grid = grid;
    this.dictionary = dictionary;
    this.solutions = new Set();
    this.invalidGrid = !this._gridIsValid(this.grid);
  }

  setGrid(grid) {
    this.grid = grid;
    this.solutions = new Set();
  }

  setDictionary(dictionary) {
    this.dictionary = dictionary;
    this.solutions = new Set();
  }

  getSolution() {
    // Ensure inputs exist
    if (!this.grid || this.dictionary === null || this.dictionary === undefined) {
      return [];
    }

    const size = this.grid.length;

    // Handle empty grid case
    if (size === 0) {
      return [];
    }

    // Grid must be square (NxN)
    if (this.grid.some(row => row.length !== size)) {
      return [];
    }

    // Normalize everything to uppercase
    const { grid: normalizedGrid, dictionary: normalizedDict } = 
      this._normalizeInput(this.grid, this.dictionary);
    this.grid = normalizedGrid;
    this.dictionary = normalizedDict;

    // Validate grid
    if (!this._gridIsValid(this.grid)) {
      return [];
    }

    // Build word set for fast lookup
    const wordSet = new Set(this.dictionary);
    const visited = Array(size).fill(null).map(() => Array(size).fill(false));

    // Explore from each grid position
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        this._search("", r, c, visited, wordSet, 0);
      }
    }

    // Return sorted solutions
    return Array.from(this.solutions).sort().map(word => word.toUpperCase());
  }

  _normalizeInput(grid, dictionary) {
    const upperGrid = grid.map(row => row.map(cell => cell.toUpperCase()));
    const upperDict = dictionary.map(word => word.toUpperCase());
    return { grid: upperGrid, dictionary: upperDict };
  }

  _gridIsValid(grid) {
    if (!grid || !Array.isArray(grid)) {
      return false;
    }
    for (let row of grid) {
      if (!Array.isArray(row)) {
        return false;
      }
      for (let cell of row) {
        if (typeof cell !== 'string' || !cell.match(/^[A-Z]+$/i)) {
          return false;
        }
        const upperCell = cell.toUpperCase();
        if (upperCell === "Q" || upperCell === "S" || upperCell === "I") {
          return false;
        }
      }
    }
    return true;
  }

  _isPrefix(prefix, wordSet) {
    for (let word of wordSet) {
      if (word.startsWith(prefix)) {
        return true;
      }
    }
    return false;
  }

  _search(current, row, col, visited, wordSet, length) {
    const n = this.grid.length;

    // Base case: stop if out of bounds or cell has already been visited
    if (row < 0 || row >= n || col < 0 || col >= n || visited[row][col]) {
      return;
    }

    // Retrieve current tile and add to current word
    const tile = this.grid[row][col].toUpperCase();
    const newWord = current + tile;

    // Update word length with special tiles
    const newLength = length + (BoggleSolver.SPECIAL_TILES[tile] || 1);

    // Prune search early if no dictionary word begins with this prefix
    if (!this._isPrefix(newWord, wordSet)) {
      return;
    }

    // Mark this cell as visited
    visited[row][col] = true;

    // If valid word is found with length requirement, add to solutions
    if (wordSet.has(newWord) && newLength >= 3) {
      this.solutions.add(newWord.toUpperCase());
    }

    // Explore all neighboring cells (8 directions)
    for (let dr = -1; dr <= 1; dr++) {
      for (let dc = -1; dc <= 1; dc++) {
        if (dr === 0 && dc === 0) {
          continue;
        }
        this._search(newWord, row + dr, col + dc, visited, wordSet, newLength);
      }
    }

    // Backtrack: unmark the cell
    visited[row][col] = false;
  }

  // Helper method to check if a word is valid on the board
  isValidWord(word) {
    const allSolutions = this.getSolution();
    return allSolutions.includes(word.toUpperCase());
  }
}

export default BoggleSolver;

