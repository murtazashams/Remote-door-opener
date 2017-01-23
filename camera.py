from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.capture("/etc/mosquitto/pgm/capture.jpg");
#camera.show("capture.jpg")
sleep(2)
camera.stop_preview()

