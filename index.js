var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var request = require('request');

global.current = 0;

app.get('/', function(req, res){
res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  console.log('a user connected');
  socket.on('disconnect', function(){//event 1
    console.log('user disconnected');
  });
  socket.on('chat message', function(msg){//event 2
    console.log('message: ' + msg);
  });
  socket.on('getVI', function(msg){//event 3
    io.emit('sentVI', { voltage: global.voltage, current: global.current });
  });
  
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});

//Update global VI in interval
setInterval(function() {
  request('http://qhsolar.duckdns.org:5000/solar', function (error, response, data) {
    if (!error && response.statusCode == 200) {
        console.log(data); 
		var jsonContent = JSON.parse(data);
		global.voltage = jsonContent.voltage;
		//console.log("jsonContent.voltage: ")
		//console.log(jsonContent.voltage);
		//console.log("Global voltage: ")
		//console.log(global.voltage);
    
     }
})
}, 1000);



    