import random
import time
# import Adafruit_SSD1306
from ina219 import INA219
from flask import Flask, jsonify
# from PIL import Image
# from PIL import ImageDraw
# from PIL import ImageFont
from multiprocessing import Process, Manager
import  RPi.GPIO as GPIO
from ctypes import c_int, c_char_p

#Configuring GPIO
#------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_UP)
#lastButton = False
#currentButton = False
#serverOn = True


#Configuring INA219
#------------------
v = 1
i = 1
ina = INA219(shunt_ohms=0.1,
             max_expected_amps = 3,
             address=0x40)

ina.configure(voltage_range=ina.RANGE_16V,
              gain=ina.GAIN_AUTO,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)

print "Done configuring INA219!"

# #Configuring OLED
# #------------------
# # Raspberry Pi pin configuration:
# RST = 24
# # 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# # Initialize library.
# disp.begin()
# # Clear display.
# disp.clear()
# disp.display()
# width = disp.width
# height = disp.height
# image = Image.new('1', (width, height))
# draw = ImageDraw.Draw(image)
# # Load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# # Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraft.ttf', 10)
#
# print "Done configuring OLED!"

#Configuring Rest API
#--------------------
app = Flask(__name__)

print "Done configuring REST API!"

#Functions declarations
#----------------------
@app.route('/solar', methods=['GET'])
def get_data(): #function that will be called when api is accessed

    global l
    localCache = l
    print ("Item from q in server proc: " + str(localCache))
    v = localCache[0]
    i = localCache[1]
    try:

        return jsonify(voltage=v,
                       current=i,
                       )

    except (IndexError, IOError) as e:
        port.flushInput()
        port.flushOutput()
        return jsonify({'error': e.message}), 503

def updateVI(d, l):#Cannot get when other process is getting
    #global v
    #global i
    #global q
    firstStart = True
    localCache = 'on'
    print "UpdateVI proc started..."
    while 1:
        print "firstStart: "
        print firstStart
        if (firstStart == False):
            print "Updating localCache in UpdateVI..."
            localCache = l[2]
            print "UpdateVI proc got cache...Server status: " + localCache
        v = ina.voltage()
        i = ina.current()
        l[0] = str(v)
        l[1] = str(i)
        l[2] = localCache
        print  'Voltage: '
        print v
        print 'Current: '
        print i
        firstStart = False
        #ina.sleep()
        time.sleep(10)
        #ina.wake()



# def localDisplay(d, l):
#     print "localDisplay proc started..."
#     while 1:
#
#         # Create new blank image for drawing.
#         # Get drawing object to draw on image.
#         global  image
#         image = Image.new('1', (width, height))
#         global  draw
#         draw = ImageDraw.Draw(image)
#
#         localCache = l
#         #localCache = [33, 33, 'on']
#         print ("Item from q in localDisp proc: " + str(l))
#         v = localCache[0]
#         i = localCache[1]
#         status = localCache[2]
#         draw.text((0,0),    'Project Solar',  font=font, fill=255)
#         draw.text((0,10),   '-----------------',  font=font, fill=255)
#         draw.text((0,20),    'Voltage: ',  font=font, fill=255)
#         draw.text((0,30),   'Current: ',  font=font, fill=255)
#         draw.text((0,40),    'Server Status: ',  font=font, fill=255)
#         draw.text((80,20),   str(v),  font=font, fill=255)
#         draw.text((80,30),   str(i),  font=font, fill=255)
#         draw.text((80,40),   status,  font=font, fill=255)
#         disp.image(image)
#         disp.display()
#
#         time.sleep(10)


def debounce(last):
    current = GPIO.input(17)
    if (last != current):
        time.sleep(0.005)
        current = GPIO.input(17)
    return current

def switchListener(d, l):

   print "Switch listener started"
   lastButton = False
   currentButton = False
   serverOn = True
   while True:
        currentButton = debounce(lastButton)
        if (lastButton == True and currentButton == False): #button is pressed
            serverOn = not serverOn
            localCache = l
            if(serverOn == False):
                serverProc.terminate()
                serverProc = 0
                l[2] = 'Off'
                print "Server terminated..."
                print "l updated: " + str(l)
            else:
                global serverProc
                serverProc = Process(target=startServer)
                serverProc.start()
                l[2] = 'On'
                print "Server re-Started..."
        lastButton = currentButton
#on off
#1

def startServer():
    print "Server process started..."
    app.run(host='0.0.0.0')




#Start of program
#---------------
print "Starting various processes now..."
if __name__ == "__main__":

   manager = Manager()
   d = manager.dict()
   list = ['0', '0', 'On']
   l = manager.list(list)
   updateVIProc = Process(target=updateVI, args=(d, l))
   serverProc = Process(target=startServer)
   # localDisplayProc = Process(target=localDisplay, args=(d, l))
   # switchListenerProc = Process(target=switchListener, args=(d, l))

   updateVIProc.start()
   time.sleep(5)
   serverProc.start()
   # localDisplayProc.start()
   # switchListenerProc.start()

   updateVIProc.join()
   serverProc.join()
   # localDisplayProc.join()
   # switchListenerProc.join()
