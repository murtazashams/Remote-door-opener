Remote door Opener using Raspberry Pi and Mosquitto MQTT

The code consists of the following modules:
camera.py : controls the camera for taking pictures. called within  client_pub
client_pub.py : publisher that publishes image through topic image and subscribes to the topic door.
client_sub.py : subcriber that subscribes to topic image and publishes to the topic door.
mosquitto1.conf : Mosquitto configuration file
mqtt_ca.key : key
mqtt_server.csr : Certificate signing request