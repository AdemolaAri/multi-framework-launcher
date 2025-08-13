import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './styles.css';

// Add error handling
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
});

try {
  const root = createRoot(document.getElementById('root'));
  root.render(<App />);
} catch (error) {
  console.error('Failed to render React app:', error);
  document.getElementById('root').innerHTML = `
    <div style="padding: 20px; color: red; font-family: Arial, sans-serif;">
      <h2>Error loading React app</h2>
      <p>${error.message}</p>
      <p>Check the browser console for more details.</p>
    </div>
  `;
}