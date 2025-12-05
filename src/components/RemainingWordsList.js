import React from 'react';

const RemainingWordsList = ({ remainingWords }) => {
  if (remainingWords.length === 0) return null;

  return (
    <div className="remaining-words-panel">
      <h2>Remaining Words ({remainingWords.length})</h2>
      <div className="words-list">
        {remainingWords.map((word, idx) => (
          <span key={idx} className="remaining-word">
            {word}
          </span>
        ))}
      </div>
    </div>
  );
};

export default RemainingWordsList;

