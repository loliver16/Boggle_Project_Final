import React from 'react';

const GameBoardCell = ({ cell, rowIdx, colIdx, isSelected, isLastSelected, onCellClick }) => {
  return (
    <div
      key={`${rowIdx}-${colIdx}`}
      className={`board-cell ${isSelected ? 'selected' : ''} ${isLastSelected ? 'last-selected' : ''}`}
      onClick={() => onCellClick(rowIdx, colIdx)}
    >
      {cell}
    </div>
  );
};

export default GameBoardCell;

