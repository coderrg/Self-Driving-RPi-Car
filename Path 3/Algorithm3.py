#Code written by Rhythm Garg

'''
###################################################################################
'''
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

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
#WE NEED ALGORITHM 2 SINCE IT IS CALLED IN ALGORITHM 3

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

def algorithm3(myLines):
    '''
    Input is a list of lines. Each line is a 4 element list:
    [x1, y1, x2, y2]
    A list of two lines (each line is [x1, y1, x2, y2])
    representing the lines of the edges of the path is returned using algorithm 3. 
    If there are not enough lines, two vertical lines are returned.
    '''
    #return vertical lines if no lines in input
    if len(myLines) < 1:
        return [[160,360,160,460],[480,360,480,460]]
    
    #return the line if one line is inputted
    if len(myLines) == 1:
        return [myLines[0], myLines[0]]
    
    #get all lines in the bottom half of the picture
    newLines = []
    for line in myLines:
        if line[1] >= 320:
            newLines.append(line)
    
    #return vertical lines if no lines left
    if len(newLines) < 1:
        return [[160,360,160,460],[480,360,480,460]]
    
    #return the line if one line is left
    if len(newLines) == 1:
        return [newLines[0], newLines[0]]
    
    #CLUSTERING ALGO
    goodSlopes = []
    lineSlopes = []

    for line in newLines:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        if (x2-x1!= 0):
            lineSlopes.append((-1)*(y2-y1)/(x2-x1))
        else:
            lineSlopes.append(1000)
        survived = True
        for slope in goodSlopes:
            if (abs(lineSlopes[-1]-slope[0]) <= 0.10):
                #find the mean slope of all the similar slopes
                slope[0] = (slope[0]*slope[1] + lineSlopes[-1])/(slope[1] + 1)
                
                #find the total number of slopes in the set of similar slopes
                slope[1] = slope[1] + 1
                
                #average x
                slope[2] = (slope[2]*(slope[1]-1) + (x1+x2)/2)/slope[1]
                
                #average y
                slope[3] = (slope[3]*(slope[1]-1) + (y1+y2)/2)/slope[1]
                
                #average x1
                slope[4] = (slope[4]*(slope[1]-1) + x1)/slope[1]
                
                #average y1
                slope[5] = (slope[5]*(slope[1]-1) + y1)/slope[1]
                
                #average x2
                slope[6] = (slope[6]*(slope[1]-1) + x2)/slope[1]
                
                #average y2
                slope[7] = (slope[7]*(slope[1]-1) + y2)/slope[1]
                
                survived = False
                break
            
        if survived:
            goodSlopes.append([lineSlopes[-1],1,(x1+x2)/2,(y1+y2)/2,x1,y1,x2,y2])
            
    #go through each line and make sure y1<y2
    for slope in goodSlopes:
        if slope[7] > slope[5]:
            tempx = slope[4]
            tempy = slope[5]
            slope[4] = slope[6]
            slope[5] = slope[7]
            slope[6] = tempx
            slope[7] = tempy
    
    #sort by avg x1
    goodSlopes.sort(key=lambda x: x[4])
    
    #return vertical lines if no lines left
    if len(goodSlopes) < 1:
        return [[160,360,160,460],[480,360,480,460]]
    
    #return the line if one line is left
    if len(goodSlopes) == 1:
        return [[goodSlopes[0][4],goodSlopes[0][5],goodSlopes[0][6],goodSlopes[0][7]],
                [goodSlopes[0][4],goodSlopes[0][5],goodSlopes[0][6],goodSlopes[0][7]]]
    
    #if there are less than 5 lines left, go ahead and send them to algorithm 2    
    if (len(goodSlopes) < 5):
        algo3Lines = []
        for slope in goodSlopes:
            algo3Lines.append([slope[4],slope[5],slope[6],slope[7]])
        return algorithm2(algo3Lines)
    
    #otherwise, let's do some more filtering!
    goingToRemove = []
    for slope1 in goodSlopes:
        for slope2 in goodSlopes:
            if slope1 is not slope2:
                min1x = min(slope1[4], slope1[6])
                min2x = min(slope2[4], slope2[6])
                #if two lines are in the same quadrant remove one of them
                if ((min1x <= 160 and min2x <= 160) or (min1x >= 480 and min2x >= 480)):
                    goingToRemove.append(goodSlopes.index(slope1))
    goingToRemove.sort()
    #remove duplicates
    goingToRemove = list(set(goingToRemove))
    goodSlopesL = len(goodSlopes)
    indexesGone = 0
    for index in goingToRemove:
        index = index % goodSlopesL
        try:
            del goodSlopes[index-indexesGone]
        except:
            print(str(index) + " - " + str(indexesGone))
            continue
        indexesGone = indexesGone + 1
    
    #return vertical lines if no lines left
    if len(goodSlopes) < 1:
        return [[160,360,160,460],[480,360,480,460]]
    
    #return the line if one line is left
    if len(goodSlopes) == 1:
        return [[goodSlopes[0][4],goodSlopes[0][5],goodSlopes[0][6],goodSlopes[0][7]],
                [goodSlopes[0][4],goodSlopes[0][5],goodSlopes[0][6],goodSlopes[0][7]]]
        
    algo3Lines = []
    for slope in goodSlopes:
        algo3Lines.append([slope[4],slope[5],slope[6],slope[7]])
    return algorithm2(algo3Lines)

'''
###################################################################################
'''


def algo3GetSlopes(image):
    '''
    Input is a 480 rows x 640 columns RGB image of the road.
    A list of two slopes (both are floats) representing the slopes
    of the lines of the edges of the path is returned. 
    '''
    plt.imshow(image)
    plt.show()
    
    file = open("Path3Algorithm3.txt", "w")
    
    #PATH 3
    imageCpy = image.copy()
    cv2.line(imageCpy, (205, 475), (450, 385), color=[255, 0, 0], thickness=2)
    cv2.line(imageCpy, (530, 480), (608, 405), color=[255, 0, 0], thickness=2)
    
    realLeftX1 = 205
    realLeftY1 = 5
    realLeftX2 = 450
    realLeftY2 = 95
    
    realRightX1 = 530
    realRightY1 = 0
    realRightX2 = 608
    realRightY2 = 75
    
    leftM = (realLeftY2 - realLeftY1)/(realLeftX2 - realLeftX1)
    leftB = realLeftY1 - leftM * realLeftX1
    
    rightM = (realRightY2 - realRightY1)/(realRightX2 - realRightX1)
    rightB = realRightY1 - rightM * realRightX1
    
    avgM = (leftM + rightM)/2
    
    file.write("The equation describing the actual left edge is y = " + str(leftM) + "x + " + str(leftB) + "\n")
    file.write("The equation describing the actual right edge is y = " + str(rightM) + "x + " + str(rightB) + "\n")
    
    cv2.imwrite("ActualEdges.jpg", imageCpy)
    
    
    blur = cv2.GaussianBlur(image,(13,13), 0)
    cv2.imwrite("2GaussianBlur.jpg", blur)
    
    edges = cv2.Canny(blur,50,100)
    cv2.imwrite("3CannyTransform.jpg", edges)
    
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
    
    allLanes = image.copy()
    for line in myLines:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        cv2.line(allLanes, (x1, y1), (x2, y2), color=[255, 0, 0], thickness=2)
    cv2.imwrite("4HoughTransform.jpg", allLanes)

    
    #black image
    output = np.zeros((480,640,3), np.uint8)
    for line in myLines:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        cv2.line(output, (x1, y1), (x2, y2), color=[255, 0, 0], thickness=2)
     
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
    
    finalEdges = algorithm3(myLines)
    image1 = image.copy()
    for line in finalEdges:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        cv2.line(image1, (int(x1), int(y1)), (int(x2), int(y2)), color=[255, 0, 0], thickness=2)
    cv2.imwrite("Algo3.jpg", image1)
    
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
    
    midLeftX = int((leftAvgLine[2] + leftAvgLine[0])/2)
    midLeftY = int((leftAvgLine[3] + leftAvgLine[1])/2)
    midRightX = int((rightAvgLine[2] + rightAvgLine[0])/2)
    midRightY = int((rightAvgLine[3] + rightAvgLine[1])/2)
    
    '''Check to make sure they are the right midpoints
    cv2.circle(image1, (midLeftX, midLeftY), 10, (0, 0, 0))
    cv2.circle(image1, (midRightX, midRightY), 10, (0, 0, 0))
    cv2.imwrite("Algo3Check.jpg", image1)
    '''
    
    file.write("\nThe midpoint of the left edge is (" + str(midLeftX) + "," + str(480-midLeftY) +")\n")
    file.write("The midpoint of the right edge is (" + str(midRightX) + "," + str(480-midRightY) +")\n")
    
    '''to calculate the shortest distance from a point to a line,
    we must use the formula d = |ax_0 + by_0 + c|/sqrt(a^2+b^2)
    Hence, we need to write our y = mx + b equations in ax + by + c = 0 form.
    This is easy; y = mx +b => mx - y + b = 0 => a = m, b = -1, c = b
    '''
    standardLeftA = leftM
    standardLeftB = -1
    standardLeftC = leftB
    
    standardRightA = rightM
    standardRightB = -1
    standardRightC = rightB
    
    performanceMeasure1 = abs(standardLeftA * midLeftX + standardLeftB * (480-midLeftY) + standardLeftC)/(math.sqrt(math.pow(standardLeftA,2) + math.pow(standardLeftB,2)))
    performanceMeasure2 = abs(standardRightA * midRightX + standardRightB * (480-midRightY) + standardRightC)/(math.sqrt(math.pow(standardRightA,2) + math.pow(standardRightB,2)))

    file.write("\nPerformance Measure 1: 1000 - " + str(performanceMeasure1)  + " = " + str(1000-performanceMeasure1) + "\n")
    file.write("\nPerformance Measure 2: 1000 - " + str(performanceMeasure2)  + " = " + str(1000-performanceMeasure2) + "\n")
    
    predictedAvg = (leftSlope + rightSlope)/2
    '''We simply need to find (predictedAvg - avgM)^2 for the third performance measure'''
    performanceMeasure3 = math.pow(predictedAvg - avgM, 2)
    
    file.write("\nPerformance Measure 3: 1000 - " + str(performanceMeasure3)  + " = " + str(1000-performanceMeasure3) + "\n")
    
    file.close()
    
    return [leftSlope, rightSlope]