#!/usr/bin/python3
# publisher

#required libraries for mqtt and AWS IoT
import sys
import ssl
import json
import os
import mosquitto as mqtt

# for motion sensor
import RPi.GPIO as GPIO
import time
from datetime import datetime

#creating a client with client-id=mqtt-test
#mqttc = mqtt.Client(client_id="test")
mqttc = mqtt.Mosquitto()

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set(ca_certs="/etc/mosquitto/certs/newcerts/mqtt_ca.crt",
                    certfile="/etc/mosquitto/certs/newcerts/mqtt_server.crt",
                    keyfile="/etc/mosquitto/certs/newcerts/mqtt_server.key",
                tls_version=ssl.PROTOCOL_TLSv1_2,
                ciphers=None)

mqttc.connect("10.22.1.143",8883,60)


#sensor = 11
#sensor2 = 13
sensor3 = 23
sensor4 = 24
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setup(sensor,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.setup(sensor2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.setup(sensor,GPIO.IN)
#GPIO.setup(sensor2,GPIO.OUT)
GPIO.setup(sensor3,GPIO.OUT)
GPIO.setup(sensor4,GPIO.OUT)





#def on_connect(mqttc, obj, flags, rc):
 #   if rc==0:
#	 mqttc.subscribe("door")
#	 print("door Subscribed ")
 #   elif rc==1:
  #      print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")

def on_message(mqttc, obj, msg):
	print ("Topic : " + msg.topic)
	i = msg.payload
#	print("AFTER msg.payload")
#	print(i)
#	GPIO.output(sensor3,GPIO.HIGH)
	if i == '7':
		print("Opening door!")
		GPIO.output(sensor3,1)
		time.sleep(80)
	        GPIO.output(sensor3,0)

    	if i == '8':
		print("Keep Door closed!")
		GPIO.output(sensor4,1)
		time.sleep(80)
		GPIO.output(sensor4,0)

	GPIO.output(sensor3,0)
	GPIO.output(sensor4,0)
# start a new thread handling communication with AWS IoT
mqttc.loop_start()

#ensor = 11
#sensor2 = 13
#3sensor3 = 5
#3sensor4 = 6
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(sensor,GPIO.IN)
#GPIO.setup(sensor2,GPIO.OUT)

mqttc.on_message = on_message

rc=0
try:
    while rc == 0:
        os.system("sudo python switch.py")
 	print("AFTER SLEEP")
        data={}
        data['motion']="button pressed"
        data['time']=datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        payload = '{"state":{"reported":'+json.dumps(data)+'}}'
        #json.dumps(data)
        print(payload)
	f = open("capture.jpg","rb")
	fileContent = f.read()
	byteArr = bytes(fileContent)
	mqttc.publish("image",byteArr,0)
        time.sleep(1)
       	mqttc.subscribe("door")
        print("door Subscribed ")
	


#mqttc.connect("129.63.17.150",8883,60)

# new code ends
except KeyboardInterrupt:
    pass

GPIO.cleanup()
ddttc.connect("10.22.1.143",8883,60)

