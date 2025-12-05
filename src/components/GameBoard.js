import React from 'react';
import GameBoardCell from './GameBoardCell';
import WordInput from './WordInput';

const GameBoard = ({
  grid,
  selectedPath,
  isSelecting,
  onCellClick,
  onToggleSelecting,
  onPathSubmit,
  onWordSubmit,
  inputWord,
  onInputChange,
  gameStopped,
  getWordFromPath,
}) => {
  return (
    <div className="board-section">
      <div className="board-container">
        <div className="boggle-board">
          {grid.map((row, rowIdx) => (
            <div key={rowIdx} className="board-row">
              {row.map((cell, colIdx) => {
                const isSelected = selectedPath.some(
                  ([r, c]) => r === rowIdx && c === colIdx
                );
                const isLastSelected = selectedPath.length > 0 &&
                  selectedPath[selectedPath.length - 1][0] === rowIdx &&
                  selectedPath[selectedPath.length - 1][1] === colIdx;

                return (
                  <GameBoardCell
                    key={`${rowIdx}-${colIdx}`}
                    cell={cell}
                    rowIdx={rowIdx}
                    colIdx={colIdx}
                    isSelected={isSelected}
                    isLastSelected={isLastSelected}
                    onCellClick={onCellClick}
                  />
                );
              })}
            </div>
          ))}
        </div>
        <div className="board-controls">
          <button
            className="btn btn-secondary"
            onClick={onToggleSelecting}
          >
            {isSelecting ? 'Stop Selecting' : 'Select Word on Board'}
          </button>
          {isSelecting && selectedPath.length > 0 && (
            <button
              className="btn btn-primary"
              onClick={onPathSubmit}
            >
              Submit: {getWordFromPath()}
            </button>
          )}
        </div>
        <WordInput
          onSubmit={onWordSubmit}
          value={inputWord}
          onChange={onInputChange}
          disabled={gameStopped}
        />
      </div>
    </div>
  );
};

export default GameBoard;

