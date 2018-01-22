#Code written by Rhythm Garg

#import libraries
from threading import Thread

from easygopigo3 import *
import time

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

from Algorithm1 import algo1GetSlopes
from Algorithm2 import algo2GetSlopes
from Algorithm3 import algo3GetSlopes
from Algorithm4 import algo4GetSlopes
 
# initialize the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)

#initialize the GoPiGo3
robot = EasyGoPiGo3()
#servo = robot.init_servo()
#distance_sensor = robot.init_distance_sensor()
min_distance = 70


def stream_video():

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
        image = frame.array
        key = cv2.waitKey(1) & 0xFF
#        cv2.imshow("Camera Input", image)

        #Choose which algorithm to use
        #laneSlopes = algo1GetSlopes(image)
        #laneSlopes = algo2GetSlopes(image)
        #laneSlopes = algo3GetSlopes(image)
        laneSlopes = algo4GetSlopes(image)
        
        slope1 = laneSlopes[0]
        slope2 = laneSlopes[1]
        
        print("-------------")
        print("slope1 is " + str(slope1)+ " and slope2 is " + str(slope2))
        if ((slope1 == 1000) or (slope1 == 0)):
            if (slope2 == 1000):
                pass
            elif (slope2 == 0):
                pass
            elif (slope2 > 0):
                print("Going forward, then turning right")
                robot.forward()
                time.sleep(2)
                robot.turn_degrees(20,True)
                time.sleep(1)
            #slope2 is negative
            else:
                print("Going forward, then turning left")
                robot.forward()
                time.sleep(2)
                robot.turn_degrees(-20,True)
                time.sleep(1)
        elif ((slope2 == 1000) or (slope2 == 0)):
            if (slope1 > 0):
                print("Going forward, then turning right")
                robot.forward()
                time.sleep(2)
                robot.turn_degrees(20,True)
                time.sleep(1)
            #slope1 is negative
            else:
                print("Going forward, then turning left")
                robot.forward()
                time.sleep(2)
                robot.turn_degrees(-20,True)
                time.sleep(1)
        else:
            if (slope1 != 1000 and slope2!= 1000 and slope1 > 0 and slope2 > 0):
                print("Going forward, then turning right")
                robot.forward()
                time.sleep(2)
                robot.turn_degrees(20,True)
                time.sleep(1)
            elif (slope1 != 1000 and slope2!= 1000 and slope1 < 0 and slope2 < 0):
                print("Going forward, then turning left")
                robot.forward()
                time.sleep(2)
                robot.turn_degrees(-20,True)
                time.sleep(1)
        print("Going forward")
        robot.forward()
        time.sleep(2)
        robot.stop()
        
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

try:
    if __name__ == "__main__":
        t1 = Thread(target = stream_video)
        t1.daemon = True
        t1.start()
        while True:
            pass
except KeyboardInterrupt:
        print("Keyboard interrupt!")
        robot.stop()
        sys.exit()
