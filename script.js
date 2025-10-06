const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = 3000; // You can change this to any port you'd like

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Sample route
app.get('/', (req, res) => {
    res.send('Welcome to the Health Access Initiative API!');
});

// Example of a POST route
app.post('/data', (req, res) => {
    const { name, age } = req.body;
    res.json({ message: Hello, ${name}. You are ${age} years old. });
});

// Start the server
app.listen(PORT, () => {
    console.log(Server is running on http://localhost:${PORT});
});