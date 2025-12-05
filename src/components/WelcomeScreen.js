import React, { useState } from 'react';

const WelcomeScreen = ({ onStartGame }) => {
  const [boardSize, setBoardSize] = useState(4);
  const [error, setError] = useState('');

  const handleSizeChange = (e) => {
    const value = parseInt(e.target.value, 10);
    if (isNaN(value) || value < 2 || value > 12) {
      setError('Board size must be between 2 and 12');
      return;
    }
    setError('');
    setBoardSize(value);
  };

  const handleStart = () => {
    if (boardSize >= 2 && boardSize <= 12) {
      onStartGame(boardSize);
    } else {
      setError('Please enter a valid board size (2-12)');
    }
  };

  return (
    <div className="welcome-screen">
      <h2>Welcome to Boggle!</h2>
      <p>Find as many words as possible in the grid</p>
      <ul className="rules-list">
        <li>Words must use adjacent tiles (including diagonals)</li>
        <li>Each tile can only be used once per word</li>
        <li>Words must be at least 3 letters long</li>
        <li>Special tiles: QU, ST, and IE count as 2 letters</li>
      </ul>
      <div className="board-size-input">
        <label htmlFor="board-size">
          Board Size (N x N):
        </label>
        <input
          id="board-size"
          type="number"
          min="2"
          max="12"
          value={boardSize}
          onChange={handleSizeChange}
          className="board-size-field"
        />
        {error && <div className="error-message">{error}</div>}
      </div>
      <button className="btn btn-start" onClick={handleStart}>
        Start Playing
      </button>
    </div>
  );
};

export default WelcomeScreen;

