#Code written by Rhythm Garg

'''The purpose of this code is to test the different algorithms'''

import cv2

from Algorithm1 import algo1GetSlopes
from Algorithm2 import algo2GetSlopes
from Algorithm3 import algo3GetSlopes
from Algorithm4 import algo4GetSlopes

image = cv2.imread("RoadViewPath3.jpg")


#print(str(algo1GetSlopes(image)))
#print(str(algo2GetSlopes(image)))
#print(str(algo3GetSlopes(image)))
print(str(algo4GetSlopes(image)))
