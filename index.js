var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var request = require('request');

global.current = 0;

app.get('/', function(req, res){
res.sendFile(__dirname + '/index.html');
});

app.use('/media', express.static(__dirname + '/media'));

io.on('connection', function(socket){
  console.log('a user connected');
  socket.on('disconnect', function(){//event 1
    console.log('user disconnected');
  });
  socket.on('chat message', function(msg){//event 2
    console.log('message: ' + msg);
  });

  socket.on('getVI', function(msg){//event 3: Client request for updates(On-demand)

	var vi = getVI(function(vi){
	//This is the callback function that will be called when getVI is called
	//So this will run at the return statement of getVI function (return  callback(...))
    //Here through the callback we get accessed to the vi obj passed in from getVI function
	//Send to client here
	//console.log("Returned vi: ")
    //console.log(vi);
	if(vi != null){
		io.emit('sentVI', { voltage: vi.voltage, current: vi.current });
		console.log("Sent VI");
		}
	else {
		io.emit('sentVI', { voltage: -1000, current: -1000 });
		console.log("Sent err VI");
	}
	});


  });

});

var port = process.env.PORT||5000; //which you can run both on Azure or local

http.listen(port, function(){
  console.log('listening on *:5000');
});

var getVI = function (callback){//Need to pass in a callback function to access return variable


	request('http://qhsolar.duckdns.org:5000/solar', function (error, response, data) {
	//request('http://192.168.1.24:5000/solar', function (error, response, data) {
		if (!error && response.statusCode == 200) {
			console.log(data);
			var jsonContent = JSON.parse(data);
			//global.voltage = jsonContent.voltage;
			console.log("jsonContent.voltage: ")
			console.log(jsonContent.voltage);
			console.log("jsonContent.current: ")
			console.log(jsonContent.current);
			return  callback({voltage: jsonContent.voltage, current: jsonContent.current});
			//console.log("rtrval: ");
			//console.log(rtrval);
			//console.log("Global voltage: ")
			//console.log(global.voltage);

		} else {

			console.log("Server Down");
			return callback(null);
		}

	});

};


/*
//Update global VI in interval
setInterval(function() {
  request('http://qhsolar.duckdns.org:5000/solar', function (error, response, data) {
    if (!error && response.statusCode == 200) {
        console.log(data);
		var jsonContent = JSON.parse(data);
		global.voltage = jsonContent.voltage;
		//console.log("jsonContent.voltage: ")
		//console.log(jsonContent.voltage);
		console.log("Global voltage: ")
		console.log(global.voltage);

     } else console.log("Server Down");
})
}, 1000);
*/
