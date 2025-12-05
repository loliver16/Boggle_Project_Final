/**
 * Generates a random Boggle board
 * @param {number} size - Size of the board (default 4 for 4x4)
 * @returns {Array<Array<string>>} - 2D array representing the board
 */
export const generateRandomBoard = (size = 4) => {
  // Standard letters (excluding Q, S, I since they must be special tiles)
  const standardLetters = 'ABCDEFGHJKLMNOPRTVWXYZ'.split('');
  
  // Special tiles that can appear
  const specialTiles = ['QU', 'ST', 'IE'];
  
  // Probability of getting a special tile (adjust as needed, currently ~15% chance)
  const specialTileProbability = 0.15;
  
  const board = [];
  
  for (let row = 0; row < size; row++) {
    const boardRow = [];
    for (let col = 0; col < size; col++) {
      // Decide if this should be a special tile
      if (Math.random() < specialTileProbability) {
        // Randomly select one of the special tiles
        const randomSpecialTile = specialTiles[Math.floor(Math.random() * specialTiles.length)];
        boardRow.push(randomSpecialTile);
      } else {
        // Select a random standard letter
        const randomLetter = standardLetters[Math.floor(Math.random() * standardLetters.length)];
        boardRow.push(randomLetter);
      }
    }
    board.push(boardRow);
  }
  
  return board;
};

/**
 * Ensures the board has at least one of each special tile type
 * This makes the game more interesting
 */
export const ensureSpecialTiles = (board) => {
  const specialTiles = ['QU', 'ST', 'IE'];
  const boardFlat = board.flat();
  
  // Check which special tiles are missing
  const missingTiles = specialTiles.filter(tile => !boardFlat.includes(tile));
  
  // If any special tiles are missing, randomly replace some cells
  if (missingTiles.length > 0) {
    let replaced = 0;
    for (let row = 0; row < board.length && replaced < missingTiles.length; row++) {
      for (let col = 0; col < board[row].length && replaced < missingTiles.length; col++) {
        // Randomly decide to replace (but not if it's already a special tile)
        if (Math.random() < 0.3 && !specialTiles.includes(board[row][col])) {
          board[row][col] = missingTiles[replaced];
          replaced++;
        }
      }
    }
    
    // If still missing, force replace random cells
    for (let i = 0; i < missingTiles.length - replaced; i++) {
      const row = Math.floor(Math.random() * board.length);
      const col = Math.floor(Math.random() * board[0].length);
      board[row][col] = missingTiles[replaced + i];
    }
  }
  
  return board;
};

/**
 * Generates a complete random board with special tiles ensured
 */
export const createRandomBoard = (size = 4) => {
  let board = generateRandomBoard(size);
  board = ensureSpecialTiles(board);
  return board;
};

