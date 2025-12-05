import React from 'react';

const WordInput = ({ onSubmit, value, onChange, disabled }) => {
  return (
    <form onSubmit={onSubmit} className="word-input-form">
      <input
        type="text"
        value={value}
        onChange={onChange}
        placeholder="Type or select a word..."
        className="word-input"
        disabled={disabled}
      />
      <button
        type="submit"
        className="btn btn-submit"
        disabled={disabled}
      >
        Submit Word
      </button>
    </form>
  );
};

export default WordInput;

