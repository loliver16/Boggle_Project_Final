import React from 'react';

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

const Timer = ({ timeLeft }) => {
  return (
    <div className="timer">
      <span className="timer-label">Time Remaining:</span>
      <span className={`timer-value ${timeLeft <= 30 ? 'warning' : ''}`}>
        {formatTime(timeLeft)}
      </span>
    </div>
  );
};

export default Timer;

