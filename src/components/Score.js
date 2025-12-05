import React from 'react';

const calculateScore = (foundWords) => {
  return foundWords.reduce((total, word) => {
    const len = word.length;
    if (len === 3 || len === 4) return total + 1;
    if (len === 5) return total + 2;
    if (len === 6) return total + 3;
    if (len === 7) return total + 5;
    return total + 11; // 8+ letters
  }, 0);
};

const Score = ({ foundWords }) => {
  return (
    <div className="score">
      <span className="score-label">Score:</span>
      <span className="score-value">{calculateScore(foundWords)}</span>
    </div>
  );
};

export default Score;

