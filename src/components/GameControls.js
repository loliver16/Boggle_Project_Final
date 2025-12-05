import React from 'react';

const GameControls = ({ gameStopped, onStopGame, onResetGame }) => {
  return (
    <div className="game-controls">
      {gameStopped ? (
        <button
          className="btn btn-start"
          onClick={onResetGame}
        >
          Reset Game
        </button>
      ) : (
        <button
          className="btn btn-stop"
          onClick={onStopGame}
        >
          Stop Game
        </button>
      )}
    </div>
  );
};

export default GameControls;

