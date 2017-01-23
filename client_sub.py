#!/usr/bin/python3
# subscriber

#required libraries for mqtt and AWS IoT
import sys
import ssl
import json
import os
import Image
import os.path
import mosquitto as mqtt
import Image as PIL


# for motion sensor
import RPi.GPIO as GPIO
import time
from datetime import datetime

#called while client tries to establish connection with the server
def on_connect(mqttc, obj, rc):
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
	mqttc.subscribe("image")     
 #  mqttc.subscribe("test", qos=0)
      # mqttc.publish("test", '{"state":{"reported":{"color":"Fu"}}}')
    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")
   #message_json['state']['reported']['color'] == "RED"


#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))

#called when a message is received by a topic
def on_message(mqttc, obj, msg):
	print ("Topic : " + msg.topic)
	f = open("output.jpg","w")
	f.write(msg.payload)
	f.close()
        os.system("sudo python viewimage.py")
  	img = Image.open("output.jpg")
	img.save("output.jpg")
	img.show()  
# publish back to publisher based on GPIO input   
	sensor = 13
	sensor2 = 19
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(sensor,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(sensor2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#	GPIO.setup(sensor,GPIO.IN)
#	GPIO.setup(sensor2,GPIO.IN)
	i = GPIO.input(sensor)
        j = GPIO.input(sensor2)
	while(i==1  and j==1):
		i = GPIO.input(sensor)
		j = GPIO.input(sensor2)
#        print(i)  
#	print(j) 
       	if(i==0):
		i = 7
		print("publish door open command")
		mqttc.publish("door",7)
		print("published")
#        j = GPIO.input(sensor2)
#        print(j) 
       	if(j==0):
                j = 8
                print("Publish door close command")
                print("published")
		mqttc.publish("door",8)


#rint("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos)+" | Data Received: "+str(msg.payload))

#creating a client with client-id=mqtt-test
#mqttc = mqtt.Client(client_id="test")
mqttc = mqtt.Mosquitto()

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message


#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set(ca_certs="/etc/mosquitto/certs/newcerts/mqtt_ca.crt",
                    certfile="/etc/mosquitto/certs/newcerts/mqtt_server.crt",
                    keyfile="/etc/mosquitto/certs/newcerts/mqtt_server.key",
                tls_version=ssl.PROTOCOL_TLSv1_2,
                ciphers=None)

#mqttc.tls_insecure_set(True)
#connecting to aws-account-specific-iot-endpoint
mqttc.connect("10.22.1.143",8883,60)
#AWS IoT service hostname and portno

#automatically handles reconnecting
rc = 0
while rc == 0:
	rc = mqttc.loop()
#mqttc.loop_forever()



