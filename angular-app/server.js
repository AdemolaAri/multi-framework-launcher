const express = require('express');
const path = require('path');
const app = express();

// Serve shared assets
app.use('/shared', express.static(path.join(__dirname, 'shared')));

// Serve static files from dist
app.use(express.static(path.join(__dirname, 'dist')));

// Handle all routes by serving index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

const PORT = process.env.PORT || 4200;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Angular-like app running on port ${PORT}`);
});