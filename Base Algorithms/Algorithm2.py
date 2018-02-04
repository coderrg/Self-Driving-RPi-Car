#Code written by Rhythm Garg

'''
###################################################################################
'''
import numpy as np
import cv2

'''
###################################################################################
'''

def makeYsGood(lines):
    '''make sure y1 is below (greater in index) y2
    takes in a list of lines, each line is [x1,y1,x2,y2]
    and retuens a list of lines such that y1 is greater 
    in index than y2''' 
    for line in lines:
        #if the value of y2 is greater than y1, then y2 is lower than y1 because of indexing
        if line[3] > line[1]:
            #switch the coordinates
            tempx = line[0]
            tempy = line[1]
            line[0] = line[2]
            line[1] = line[3]
            line[2] = tempx
            line[3] = tempy
    return lines


'''
###################################################################################
'''

def averageLine(lines):
    '''
    Input is a list of lines. Each line is a 4 element list:
    [x1, y1, x2, y2]
    A list [x1, y1, x2, y2] representing the average line of 
    the inputted lines is returned. If there are no lines, None
    is returned.
    '''
    numLines = len(lines)
    if numLines == 0:
        return None
    
    sumX1 = 0
    sumY1 = 0
    sumX2 = 0
    sumY2 = 0
    
    for line in lines:
        sumX1 = sumX1 + line[0]
        sumY1 = sumY1 + line[1]
        sumX2 = sumX2 + line[2]
        sumY2 = sumY2 + line[3]
        
    avgX1 = sumX1/numLines
    avgY1 = sumY1/numLines
    avgX2 = sumX2/numLines
    avgY2 = sumY2/numLines
    
    avgLine = [avgX1, avgY1, avgX2, avgY2]
    return avgLine

'''
###################################################################################
'''

def algorithm2(myLines):
    '''
    Input is a list of lines. Each line is a 4 element list:
    [x1, y1, x2, y2]
    A list of two lines (each line is [x1, y1, x2, y2])
    representing the lines of the edges of the path is returned using algorithm 2. 
    If there are not enough lines, two vertical lines are returned.
    '''
    if len(myLines) < 1:
        return [[160,360,160,460],[480,360,480,460]]
    
    if len(myLines) == 1:
        return [myLines[0], myLines[0]]
    
    leftLines = []
    rightLines = []
    
    for line in myLines:
        #it's in the left half and bottom half
        if line[0] <= 320 and line[1] >= 240:
            leftLines.append(line)
        #it's in the right half and bottom half
        elif line[0] > 320 and line[1] >= 240:
            rightLines.append(line)
    
    if (len(leftLines) < 1 or len(rightLines) < 1):
        return [myLines[0], myLines[-1]]
    
    leftAvgLine = averageLine(leftLines)
    rightAvgLine = averageLine(rightLines)
    
    lanes = [leftAvgLine, rightAvgLine]
    
    #make ys good
    lanes = makeYsGood(lanes)
    
    #sort by x1
    lanes.sort(key=lambda x: x[0])


    return lanes

'''
###################################################################################
'''


def algo2GetSlopes(image):
    '''
    Input is a 480 rows x 640 columns RGB image of the road.
    A list of two slopes (both are floats) representing the slopes
    of the lines of the edges of the path is returned using algorithm 2. 
    '''
    blur = cv2.GaussianBlur(image,(13,13), 0)
    #cv2.imwrite("2GaussianBlur.jpg", blur)
    
    edges = cv2.Canny(blur,100,300)
    #cv2.imwrite("3CannyTransform.jpg", edges)
    
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40, np.array([]), minLineLength=10, maxLineGap=50)
    
    #input for algorithms
    myLines = []
    for line in lines:
        nextLine = []
        lineTemp = line[0]
        nextLine.append(lineTemp[0])
        nextLine.append(lineTemp[1])
        nextLine.append(lineTemp[2])
        nextLine.append(lineTemp[3])
        myLines.append(nextLine)
    
    '''Only needed to visualize Hough Lines
    allLanes = image.copy()
    for line in myLines:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        cv2.line(allLanes, (x1, y1), (x2, y2), color=[255, 255, 255], thickness=2)
    cv2.imwrite("4HoughTransform.jpg", allLanes)
    '''
    
    #black image
    output = np.zeros((480,640,3), np.uint8)
    for line in myLines:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        cv2.line(output, (x1, y1), (x2, y2), color=[255, 255, 255], thickness=2)
     
    '''no longer needed since we are only using black and white for our neural net input image
    gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("5Output.jpg", gray_output)
    '''
    #make ys good
    myLines = makeYsGood(myLines)
    
    #sort by x1
    myLines.sort(key=lambda x: x[0])
    
    
    '''
    ###################################################################################
    '''
    #NOW WE CHOOSE THE ALGORITHM
    
    finalEdges = algorithm2(myLines)
    image1 = image.copy()
    for line in finalEdges:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        cv2.line(image1, (int(x1), int(y1)), (int(x2), int(y2)), color=[255, 255, 255], thickness=2)
    cv2.imwrite("Algo2.jpg", image1)
    
    leftAvgLine = finalEdges[0]
    rightAvgLine = finalEdges[1]
    
    try:
        leftSlope= (-1)*(leftAvgLine[3]-leftAvgLine[1])/(leftAvgLine[2]-leftAvgLine[0])
    except: 
        leftSlope = 1000
    
    try:
        rightSlope= (-1)*(rightAvgLine[3]-rightAvgLine[1])/(rightAvgLine[2]-rightAvgLine[0])
    except:
        rightSlope = 1000
    
    return [leftSlope, rightSlope]
