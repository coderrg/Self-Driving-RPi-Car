#Code written by Rhythm Garg

import numpy as np
import cv2
from scipy.misc import imresize
from keras.models import load_model

x1Start = -1
x1End = -1
y1Start = -1
y1End = -1

x2Start = -1
x2End = -1
y2Start = -1
y2End = -1

def Algorithm4(image):
    """ Takes in a road image in black and white with the hough lines of the original road image,
    resizes the input picture to 80 rows x 160 columns for the convolutional neural network model,
    predicts the lane to be drawn from the model in green, 
    and then draws lane lines using the image with the road lane shaded in green.
    It returns a list: the two slopes [slope1, slope2] of the left and right lane lines 
    """
    # Load Keras model
    model = load_model('full_CNN_model_2.h5')

    # Get image ready for feeding into model
    small_img = imresize(image, (80, 160, 3))
    small_img = np.array(small_img)    
    small_img = small_img[None,:,:,:]

    # Make prediction with neural network (un-normalize value by multiplying by 255)
    prediction = model.predict(small_img)[0] * 255
        
    # Generate fake R & B color dimensions, stack with G
    blanks = np.zeros_like(prediction).astype(np.uint8)
    lane_drawn = np.dstack((blanks, prediction, blanks))

    # Re-size to match the original image
    lane_image = imresize(lane_drawn, (480, 640, 3))
    
    ####################################################################
    global x1Start
    x1Start = 0
    global y1Start 
    y1Start = 5
    global x2Start
    x2Start = 0
    global y2Start
    y2Start = 5
    
    #which row to look at
    rowStart = 480 - y1Start - 1
    
    #find x1Start
    count = 0
    for pixel in lane_image[rowStart]:
        #640 columns
        if count < 634:
            #check to see if the point and the next 5 points are solid green
            works = True
            extra = 0
            while (extra < 6):
                if lane_image[rowStart][count+extra][1] < 150:
                    works = False
                    break
                extra = extra + 1
            if (works):
                x1Start = count
                break
        count = count + 1
            
    #find x2Start
    count = 639
    for pixel in lane_image[rowStart]:
        #160 columns
        if count > 4:
            #check to see if the point and the next 5 points are solid green
            works = True
            extra = 0
            while (extra < 6):
                if lane_image[rowStart][count-extra][1] < 150:
                    works = False
                    break
                extra = extra + 1
            if (works):
                x2Start = count
                break
        count = count - 1
        
    y1Start = 480 - y1Start - 1
    y2Start = 480 - y2Start - 1
    '''
    print(x1Start)
    print(y1Start)
    print(x2Start)
    print(y2Start)
    '''
    ####################################################################
    
    global x1End
    x1End = 0
    global y1End
    y1End = 80
    global x2End
    x2End = 0
    global y2End
    y2End = 80
    
    #which row to look at
    rowStart = 480 - y1End - 1
    
    #find x1End
    count = 0
    for pixel in lane_image[rowStart]:
        #640 columns
        if count < 634:
            #check to see if the point and the next 5 points are solid green
            works = True
            extra = 0
            while (extra < 6):
                if lane_image[rowStart][count+extra][1] < 150:
                    works = False
                    break
                extra = extra + 1
            if (works):
                x1End = count
                break
        count = count + 1
            
    #find x2End
    count = 639
    for pixel in lane_image[rowStart]:
        #160 columns
        if count > 4:
            #check to see if the point and the next 5 points are solid green
            works = True
            extra = 0
            while (extra < 6):
                if lane_image[rowStart][count-extra][1] < 150:
                    works = False
                    break
                extra = extra + 1
            if (works):
                x2End = count
                break
        count = count - 1
    
    y1End = 480 - y1End - 1
    y2End = 480 - y2End - 1
    '''
    print("------")
    print(x1End)
    print(y1End)
    print(x2End)
    print(y2End)
    '''
    ####################################################################

    # Merge the lane drawing onto the original image
    result = cv2.addWeighted(image, 1, lane_image, 1, 0)
    
    cv2.imwrite('CNNImage.jpg', result)

    #black image
    #blackBack = np.zeros((480,640,3), np.uint8)
    #blackBackResult = cv2.addWeighted(blackBack, 1, lane_image, 1, 0)
    
    #this is simply what the green shaded area of the road lane on a black background
    #cv2.imwrite('BlackBack.jpg', blackBackResult)

    try:    
        leftAvgSlope = (y1Start - y1End)/(x1End - x1Start)
    except:
        leftAvgSlope = 1000
    try:
        rightAvgSlope = (y2Start - y2End)/(x2End - x2Start)
    except:
        rightAvgSlope= 1000
    return [leftAvgSlope, rightAvgSlope]
    
    #return realLanes
    
def algo4GetSlopes(image):
    '''
    Input is a 480 rows x 640 columns RGB image of the road.
    A list of two slopes (both are floats) representing the slopes
    of the lines of the edges of the path is returned using algorithm 4 
    (convolutional neural network). 
    '''
    
    #we only care about the bottom half of the 480 rows x 640 columns image
    #image = image[240:,:]
    
    #don't resize because that will cause distortion and loss of accuracy
    #image = imresize(image, (480, 640, 3))

    #cv2.imwrite("INPUT.jpg",image)

    #imgCopy = image.copy()

    blur = cv2.GaussianBlur(image,(13,13), 0)
    #cv2.imwrite("GAUSS.jpg",blur)

    edges = cv2.Canny(blur,10,100)
    #cv2.imwrite("CANNNY.jpg",edges)
    
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40, np.array([]), minLineLength=10, maxLineGap=50)
    #cv2.imwrite('HOUGH.jpg',lines)        

    myLines = []
    try:
        for line in lines:
            nextLine = []
            lineTemp = line[0]
            nextLine.append(lineTemp[0])
            nextLine.append(lineTemp[1])
            nextLine.append(lineTemp[2])
            nextLine.append(lineTemp[3])
            myLines.append(nextLine)
    except:
        print("No lines found!")

    #black image
    output = np.zeros((480,640,3), np.uint8)
    for line in myLines:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        cv2.line(output, (x1, y1), (x2, y2), color=[255, 255, 255], thickness=2)
     
    #for the neural net
    #gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    
    #this is the actual neural net input
    #cv2.imwrite("NeuralNetInput.jpg", output)

    lines = Algorithm4(np.array(output))
    
    #black image
    realLanes = image.copy()
    cv2.line(realLanes, (x1Start, y1Start), (x1End, y1End), color=[255, 255, 255], thickness=2)
    cv2.line(realLanes, (x2Start, y2Start), (x2End, y2End), color=[255, 255, 255], thickness=2)
    cv2.imwrite('Algo4.jpg', realLanes)
    
    return lines
