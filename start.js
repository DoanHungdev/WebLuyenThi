const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const dbPath = path.join(__dirname, 'backend', 'db', 'database.sqlite');

if (!fs.existsSync(dbPath)) {
  console.log('Database not found. Running initialization...');
  try {
    execSync('node backend/init_db.js', { stdio: 'inherit' });
    console.log('Database initialized successfully.');
  } catch (err) {
    console.error('Failed to initialize database:', err);
  }
} else {
  console.log('Database found. Skipping initialization.');
}

console.log('Starting Express server...');
require('./backend/server.js');
