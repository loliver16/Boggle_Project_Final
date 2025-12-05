import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Boggle Game header', () => {
  render(<App />);
  const headerElement = screen.getByText(/Boggle Game/i);
  expect(headerElement).toBeInTheDocument();
});

test('renders welcome screen', () => {
  render(<App />);
  const welcomeElement = screen.getByText(/Welcome to Boggle!/i);
  expect(welcomeElement).toBeInTheDocument();
});

test('renders start playing button', () => {
  render(<App />);
  const startButton = screen.getByText(/Start Playing/i);
  expect(startButton).toBeInTheDocument();
});
