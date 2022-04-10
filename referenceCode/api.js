module.exports = app => {
    const sql = require("./db.js");
  
    var router = require("express").Router();
  
    router.get("/select/page", (req, res) => {
        let query = "SELECT * FROM page where page_id = ?";

        sql.query(query, req.query.id, (err, result) => {
            if (err) {
            console.log("error: ", err);
            res.status(500).send(err);
            return;
            }

            res.send(result);
        });
    });
  
    router.post("/insert/page", (req, res) => {
        let query = "INSERT INTO page SET ?";

        sql.query(query, req.body, (err, result) => {
            if (err) {
            console.log("error: ", err);
            res.status(500).send(err);
            return;
            }

            res.send(result);
        });
    });
  
    router.post("/update/page", (req, res) => {
        let query = "UPDATE page SET ? WHERE page_id = ?";

        sql.query(query, [req.body, req.body.page_id], (err, result) => {
            if (err) {
            console.log("error: ", err);
            res.status(500).send(err);
            return;
            }

            res.send(result);
        });
    });
  
    router.post("/delete/page", (req, res) => {
        let query = "DELETE FROM page WHERE?";
        var parameters = req.body;
        var attributes = [page_id];

        if (!attributes.every(a => parameters.includes(a))){
            console.log('error: ', 'Attributes not match');
            res.status(500).send('Attributes not match');
            return;
        }

        Object.keys(parameters).filter(k => attributes.includes(k)).reduce((c, k) => {return Object.assign(c, {[k]: parameters[k]}, {})});

        sql.query(query, parameters, (err, result) => {
            if (err) {
            console.log("error: ", err);
            res.status(500).send(err);
            return;
            }

            res.send(result);
        });
    });
    
    app.use('/', router);
  };