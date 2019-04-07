# Project-Solar
A system to track and visalize battery charging/usage of a 50W Solar setup. 

The power data is collected via the INA169 Analog DC Current Sensor which is connected to a Raspberry Pi 3 (RPI3) via the I2C interface. The RPI3 is running a Python based HTTP server which provides a RESTful interface which can be accessed to retrieve the power data. A sample NodeJS websever is built to retrieve data from the RPI3 via the RESTful interface which it will present the data in the form of a webpage.

The Setup

![alt text](https://raw.githubusercontent.com/laiqinghui/Project-Solar/master/media/panel.jpg)




