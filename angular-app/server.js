const express = require('express');
const path = require('path');
const app = express();

// Serve shared assets
app.use('/shared', express.static(path.join(__dirname, 'shared')));

// Serve static files from dist
app.use(express.static(path.join(__dirname, 'dist')));

// Handle SPA routes by serving index.html for non-file requests
app.get('*', (req, res) => {
  // If the request is for a file with an extension, let express.static handle it
  if (path.extname(req.path)) {
    res.status(404).send('File not found');
  } else {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
  }
});

const PORT = process.env.PORT || 4200;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Angular-like app running on port ${PORT}`);
});