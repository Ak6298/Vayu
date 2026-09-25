const express = require('express');
const mysql = require('mysql2/promise');
const path = require('path');

const app = express();
const port = process.env.PORT || 5500;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname)));

app.use((err, req, res, next) => {
  if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
    return res.status(400).json({ success: false, message: 'Invalid JSON payload.' });
  }
  next(err);
});

const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || 'root',
  database: process.env.DB_NAME || 'travel_app',
  port: Number(process.env.DB_PORT || 3306),
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
};

let pool = null;

async function initializeDatabase() {
  const adminConfig = {
    host: dbConfig.host,
    user: dbConfig.user,
    password: dbConfig.password,
    port: dbConfig.port,
    waitForConnections: true,
    connectionLimit: 5,
  };

  try {
    const adminPool = mysql.createPool(adminConfig);
    await adminPool.query(`CREATE DATABASE IF NOT EXISTS \`${dbConfig.database}\``);
    await adminPool.end();

    pool = mysql.createPool(dbConfig);

    await pool.execute(`
      CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        email VARCHAR(150) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);

    console.log('MySQL connected and users table is ready.');
  } catch (error) {
    console.error('MySQL not available yet. Please start MySQL and update your credentials in .env or server.js.');
    console.error(error.message);
    pool = null;
  }
}

function isDatabaseReady() {
  return !!pool;
}

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'home-page.html'));
});

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

app.get('/register', (req, res) => {
  res.sendFile(path.join(__dirname, 'register.html'));
});

app.post('/api/register', async (req, res) => {
  const { name, phone, email, password } = req.body;

  if (!name || !phone || !email || !password) {
    return res.status(400).json({ success: false, message: 'All fields are required.' });
  }

  if (!isDatabaseReady()) {
    return res.status(503).json({
      success: false,
      message: 'MySQL is not connected. Please start the database and try again.',
    });
  }

  try {
    const [existingUsers] = await pool.execute('SELECT id FROM users WHERE email = ?', [email]);

    if (existingUsers.length > 0) {
      return res.status(409).json({ success: false, message: 'This email is already registered.' });
    }

    const [result] = await pool.execute(
      'INSERT INTO users (name, phone, email, password) VALUES (?, ?, ?, ?)',
      [name, phone, email, password]
    );

    res.status(201).json({
      success: true,
      message: 'Registration successful.',
      userId: result.insertId,
    });
  } catch (error) {
    console.error('Register error:', error);
    res.status(500).json({ success: false, message: 'Registration failed. Please try again later.' });
  }
});

app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ success: false, message: 'Email and password are required.' });
  }

  if (!isDatabaseReady()) {
    return res.status(503).json({
      success: false,
      message: 'MySQL is not connected. Please start the database and try again.',
    });
  }

  try {
    const [rows] = await pool.execute(
      'SELECT id, name, phone, email, password FROM users WHERE email = ? AND password = ?',
      [email, password]
    );

    if (rows.length === 0) {
      return res.status(401).json({ success: false, message: 'Invalid email or password.' });
    }

    const user = rows[0];
    res.json({
      success: true,
      message: 'Login successful.',
      user: {
        id: user.id,
        name: user.name,
        phone: user.phone,
        email: user.email,
      },
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ success: false, message: 'Login failed. Please try again later.' });
  }
});

app.use((req, res) => {
  res.status(404).json({ success: false, message: 'Route not found.' });
});

initializeDatabase().then(() => {
  app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
  });
});
