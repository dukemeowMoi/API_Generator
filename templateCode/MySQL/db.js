// mysql version
const mysql = require("mysql");

const connection = mysql.createConnection({
  host: '[hostname]',
  user: '[username]',
  password: '[password]',
  database: '[database]'
});

connection.connect(error => {
  if (error) throw error;
  console.log("Successfully connected to the database.");
});

module.exports = connection;