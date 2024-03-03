const express = require("express");
const app = express();
var api = require("./api.js");
app.use('/api', api);

// const activeUsers = {}; // Replace Redis client with a simple object

// const db_queries = require('./db.js');
// const db = new db_queries();

app.use(express.static("public"));

var bodyParser = require("body-parser");

var urlencodedParser = bodyParser.urlencoded({ extended: false });
app.use(urlencodedParser);
app.use(bodyParser.json());

app.get("/", function (req, res) {
    res.sendFile(__dirname + "/views/index.html");
});
    
app.listen(3000, function () {
    console.log("Example app listening on port 3000!");
});