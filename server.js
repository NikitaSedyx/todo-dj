var express = require("express");
var bodyParser = require('body-parser');
var fs = require("fs");
var _ = require("underscore");

var httpProxy = require('http-proxy');
var apiProxy = httpProxy.createProxyServer();

var app = express();

app.use(express.static('build'));
app.use(bodyParser.json());

app.get("/", function(req, res){
  res.sendFile(__dirname + "/build/index.html")
});
 
app.all("/*", function(req, res){ 

  req.removeAllListeners('data');
  req.removeAllListeners('end');

  process.nextTick(function () {
    if(req.body) {
      req.emit('data', JSON.stringify(req.body));
    }
    req.emit('end');
  });
  apiProxy.web(req, res, { target: 'http://0.0.0.0:8080'});
});

var port = process.env.PORT || 5000
app.listen(port, '0.0.0.0', function(){
  console.log("Started in " + port)
});



/*
var tasksJSON = require("./tasks.json");
var isFirst = !tasksJSON.length ? true : false;

app.get("/tasks", function(req, res){
  fs.readFile('./tasks.json', 'utf8', function (err,buffer) {
    res.send(buffer);
  })
});

app.post("/tasks", function(req, res){
  var data = req.body;
  fs.stat('./tasks.json', function(err, stats){
    fs.truncate('./tasks.json', stats["size"]-1, function(err){
      if (err) return err;
      var line = JSON.stringify(data)+"]";
      if (isFirst){
        isFirst = false;
      }else{
        line = "," + line;
      }
      fs.appendFile('./tasks.json', line, function(err){
        if (err) return err;
      });
    });
  });
  res.send("ok")
  res.status(200);
});

app.get("/tasks/:id", function(req, res){
  var tasks = []
  fs.readFile('./tasks.json', 'utf8', function (err,buffer) {
    tasks = JSON.parse(buffer)
    var task = _.find(tasks, function(task){
      return task.id === req.params.id
    })  
    res.json(task)
  })
});

app.put("/tasks/:id", function(req, res){
  var taskId = req.params.id
  var editedTask = req.body
  fs.readFile('./tasks.json', 'utf8', function (err,buffer) {
    tasks = JSON.parse(buffer)
    var task = _.find(tasks, function(task){
      return task.id === taskId
    })  
    tasks[_.indexOf(tasks, task)] = editedTask
    fs.writeFile('./tasks.json', JSON.stringify(tasks), 'utf8', function (err) {
      if (err) return console.log(err);
    });
  })
})

app.delete("/tasks/:id", function(req, res){
  var taskId = req.params.id
  fs.readFile('./tasks.json', 'utf8', function (err,buffer) {
    tasks = JSON.parse(buffer)
    var task = _.find(tasks, function(task){
      return task.id === taskId
    })  
    tasks.splice(_.indexOf(tasks, task),1)
    fs.writeFile('./tasks.json', JSON.stringify(tasks), 'utf8', function (err) {
      if (err) return console.log(err);
      fs.readFile('./tasks.json', function(err, buffer){
        isFirst = !JSON.parse(buffer).length ? true : false;
      })
    });
  })
})*/


