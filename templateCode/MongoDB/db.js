// mongoDB version
const mongoDB = require("mongodb");

const uri = "[connectionStr]";

const client = new mongoDB.MongoClient(uri);

let database;

module.exports = {
    getConnection: function(){ 
        return new Promise(function(resolve, reject){
            client.connect(function(err, db) {
                if (err || !db) {
                    return reject(err);
                }
            
                database = db.db('[database]');

                resolve(database)
            })
        })
    },
    mongoDB: mongoDB,
}
