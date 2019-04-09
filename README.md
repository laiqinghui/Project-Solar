# Project-Solar
A system to track and visalize battery charging/usage of a 50W Solar setup. 

The power data is collected via the INA169 Analog DC Current Sensor which is connected to a Raspberry Pi 3 (RPI3) via the I2C interface. The RPI3 serves as a gateway for the sensor and was configured to run a Python based HTTP server which provides a RESTful interface for any HTTP based client to retrieve the latest sensor data.

A NodeJS websever is built to host a web application which will display the data retrieved off the RPI3 in real-time or on demand. Data is stream off the the webserver to the client browser via web-socket.


<img src="https://raw.githubusercontent.com/laiqinghui/Project-Solar/master/media/Block.JPG" alt="alt text" width="100%" height="500">



The Components

<img src="https://raw.githubusercontent.com/laiqinghui/Project-Solar/master/media/Overall.jpg" alt="alt text" width="600" height="450"> 
 
<img src="https://raw.githubusercontent.com/laiqinghui/Project-Solar/master/media/rpi.jpg" alt="alt text" width="600" height="450">

<img src="https://raw.githubusercontent.com/laiqinghui/Project-Solar/master/media/mppt.jpg" alt="alt text" width="600" height="450">



 
