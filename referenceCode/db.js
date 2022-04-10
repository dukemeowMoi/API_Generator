// mysql version
const mysql = require("mysql");

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'ma',
  password: '789987',
  database: 'fyp'
});

connection.connect(error => {
  if (error) throw error;
  console.log("Successfully connected to the database.");
});

module.exports = connection;