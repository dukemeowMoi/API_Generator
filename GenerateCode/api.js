module.exports = app => {
  const sql = require("./db.js");

  var router = require("express").Router();

  router.get('/select/page', (req, res) => {
var parameters = req.query;
let query = 'SELECT page_title,page_content FROM Page where [cons]';
var constraints = ['page_id'];
if (!constraints.every(a => Object.keys(parameters).includes(a))){
console.log('error: ', 'Constraints not match');res.status(500).send('Constraints not match');return;}
var cons = Object.fromEntries(Object.entries(parameters).filter(([k]) => constraints.includes(k)));
if (Object.keys(cons).length == 0) cons[1] = 1;var keys = Object.keys(cons).map(k => k + '= ?');
query = query.replace('[cons]', keys.join(' AND '));
sql.query(query,Object.values(cons),(err,result)=>{if(err){console.log('error:',err);res.status(500).send(err);return;}res.send(result);});
});
router.post('/insert/page', (req, res) => {
var parameters = req.body;
let query = 'INSERT INTO Page set ?';
var attributes = ['page_slug','page_title','page_content'];
if (!attributes.every(a => Object.keys(parameters).includes(a)) || attributes.length == 0){
console.log('error: ', 'Attributes not match');res.status(500).send('Attributes not match');return;}
var atts = Object.fromEntries(Object.entries(parameters).filter(([k]) => attributes.includes(k)));
sql.query(query,atts,(err,result)=>{if(err){console.log('error:',err);res.status(500).send(err);return;}res.send(result);});
});
router.post('/update/page', (req, res) => {
var parameters = req.body;
let query = 'Update Page SET ? where [cons]';
var attributes = ['page_slug','page_title','page_content'];
if (!attributes.every(a => Object.keys(parameters).includes(a)) || attributes.length == 0){
console.log('error: ', 'Attributes not match');res.status(500).send('Attributes not match');return;}
var atts = Object.fromEntries(Object.entries(parameters).filter(([k]) => attributes.includes(k)));
var constraints = ['page_id'];
if (!constraints.every(a => Object.keys(parameters).includes(a))){
console.log('error: ', 'Constraints not match');res.status(500).send('Constraints not match');return;}
var cons = Object.fromEntries(Object.entries(parameters).filter(([k]) => constraints.includes(k)));
if (Object.keys(cons).length == 0) cons[1] = 1;var keys = Object.keys(cons).map(k => k + '= ?');
query = query.replace('[cons]', keys.join(' AND '));
sql.query(query,[atts, Object.values(cons)],(err,result)=>{if(err){console.log('error:',err);res.status(500).send(err);return;}res.send(result);});
});
router.post('/delete/page', (req, res) => {
var parameters = req.body;
let query = 'DELETE FROM Page where [cons]';
var constraints = ['page_id'];
if (!constraints.every(a => Object.keys(parameters).includes(a))){
console.log('error: ', 'Constraints not match');res.status(500).send('Constraints not match');return;}
var cons = Object.fromEntries(Object.entries(parameters).filter(([k]) => constraints.includes(k)));
if (Object.keys(cons).length == 0) cons[1] = 1;var keys = Object.keys(cons).map(k => k + '= ?');
query = query.replace('[cons]', keys.join(' AND '));
sql.query(query,Object.values(cons),(err,result)=>{if(err){console.log('error:',err);res.status(500).send(err);return;}res.send(result);});
});
router.get('/get/menu', (req, res) => {
var parameters = req.query;
let query = 'SELECT page_slug,page_title FROM Page where [cons]';
var constraints = [];
if (!constraints.every(a => Object.keys(parameters).includes(a))){
console.log('error: ', 'Constraints not match');res.status(500).send('Constraints not match');return;}
var cons = Object.fromEntries(Object.entries(parameters).filter(([k]) => constraints.includes(k)));
if (Object.keys(cons).length == 0) cons[1] = 1;var keys = Object.keys(cons).map(k => k + '= ?');
query = query.replace('[cons]', keys.join(' AND '));
sql.query(query,Object.values(cons),(err,result)=>{if(err){console.log('error:',err);res.status(500).send(err);return;}res.send(result);});
});
router.post('/add/page2', (req, res) => {
var parameters = req.body;
let query = 'INSERT INTO Page set ?';
var attributes = ['page_slug','page_title'];
if (!attributes.every(a => Object.keys(parameters).includes(a)) || attributes.length == 0){
console.log('error: ', 'Attributes not match');res.status(500).send('Attributes not match');return;}
var atts = Object.fromEntries(Object.entries(parameters).filter(([k]) => attributes.includes(k)));
sql.query(query,atts,(err,result)=>{if(err){console.log('error:',err);res.status(500).send(err);return;}res.send(result);});
});

  
  app.use('/', router);
};


