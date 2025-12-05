import React from 'react';

const FoundWordsList = ({ foundWords }) => {
  return (
    <div className="found-words-panel">
      <h2>Found Words ({foundWords.length})</h2>
      <div className="words-list">
        {foundWords.length === 0 ? (
          <p className="empty-message">No words found yet...</p>
        ) : (
          foundWords.map((word, idx) => (
            <span key={idx} className="found-word">
              {word}
            </span>
          ))
        )}
      </div>
    </div>
  );
};

export default FoundWordsList;

