import numpy as np
import cv2
#import time

#'''
def getColorAve(array):
    #This method returns the average of a NxN box of colors as a pixel, RGB
    arr = np.array(array)
    return np.mean(np.mean(arr, axis = 1), axis = 0)

def checkIfBoxIsCloseToCharacter(character, box, tolerance):
    #Takes the box and finds how close the difference of every RBG value to the character
    #Then checks if that difference is less than some tolerance for R,G, and B
    return np.count_nonzero(abs(box - character) < (np.ones(3) * tolerance)) == 3

def checkAroundCord(img, cord, boxLength, character, tolerance, numWanted):
    frame = img
    #If there are a certain amount of close boxes in an area, end.
    if(len(closeBoxes) > numWanted):
        return    
    #Finds a cord about half a box away from our curent cord.
    #In our example, it would find a cord 2 pixels to the right (5 by 5 box), boxLength = 5
    rCord = [cord[0] + int(boxLength/2), cord[1]]
    #Only do any computational or recursive work on the corrdiante if it hasn't arlready been checked
    if(not(rCord in closeBoxes)):
        #Selects a box that starts at those cordinates we just found and goes for box Lenght pixels in both  directions
        rBox = frame[rCord[1]: rCord[1] + boxLength, rCord[0]: rCord[0] + boxLength]
        #Stores the average pixel into a Variable
        rAve = getColorAve(rBox)
        #Check if the average of the box is close to the character color
        rClose = checkIfBoxIsCloseToCharacter(character, rAve, tolerance)
        #If the box is close
        if(rClose):
            #Add it to the closeBoxes list so it isn't checked multipe times
            closeBoxes.append(rCord)
            #Recursively check it and points aroun it.
            checkAroundCord(frame, rCord, boxLength, character, tolerance, numWanted)

    #Does that same thing for each of the cardinal directions
    lCord = [cord[0] - int(boxLength/2), cord[1]]
    if(not(lCord in closeBoxes)):
        lBox = frame[lCord[1]: lCord[1] + boxLength, lCord[0]: lCord[0] + boxLength]
        lAve = getColorAve(lBox)
        lClose = checkIfBoxIsCloseToCharacter(character, lAve, tolerance)
        if(lClose):
            closeBoxes.append(lCord)
            checkAroundCord(frame, lCord, boxLength, character, tolerance, numWanted)

    uCord = [cord[0], cord[1] - int(boxLength/2)]
    if(not(uCord in closeBoxes)):
        uBox = frame[uCord[1]: uCord[1] + boxLength, uCord[0]: uCord[0] + boxLength]
        uAve = getColorAve(uBox)
        uClose = checkIfBoxIsCloseToCharacter(character, uAve, tolerance)
        if(uClose):
            closeBoxes.append(uCord)
            checkAroundCord(frame, uCord, boxLength, character, tolerance, numWanted)

    dCord = [cord[0], cord[1] + int(boxLength/2)]
    if(not(dCord in closeBoxes)):
        dBox = frame[dCord[1]: dCord[1] + boxLength, dCord[0]: dCord[0] + boxLength]
        dAve = getColorAve(dBox)
        dClose = checkIfBoxIsCloseToCharacter(character, dAve, tolerance)
        if(dClose):
            closeBoxes.append(dCord)
            checkAroundCord(frame, dCord, boxLength, character, tolerance, numWanted)

def searchFromCords(img,x,y,boxLength, tolerance, numWanted, moveDist, direction):
    #We Have to look at coordinate y,x because rows are displayed up and down aka Y and columns are displayed left and right aka X.
    #Gives us a pixel value [B,G,R]
    #print(frame[y,x])

    #print("Spot:" + str([x,y]))

    spotsChecked.append([x,y])
    
    #The "Average" Color of our Character, Azoth
    character = [183.298, 173.652, 159.09]
    character = np.array(character)

    checkAroundCord(img,[x,y], boxLength, character, tolerance, numWanted)
    
    '''
    if(x >= 0 and y >= 0):
        checkAroundCord(img,[x,y], boxLength, character, tolerance, numWanted)
    else:
        print(spotsChecked[-1])
    #'''

    isCharacter = len(closeBoxes) >= numWanted
    #print("Is There a Character? " + str(isCharacter))
    if(isCharacter):
        return isCharacter, [x,y]
    else:
        if(direction == 0):
            newCords = [x, y - moveDist]
        elif(direction == 1):
            newCords = [x - moveDist, y]
        elif(direction == 2):
            newCords = [x, y + moveDist]
        else:
            newCords = [x + moveDist, y]
        if(newCords in spotsChecked):
            if((direction - 1) % 4 == 0):
                newCords = [x, y - moveDist]
            elif((direction - 1) % 4 == 1):
                newCords = [x - moveDist, y]
            elif((direction - 1) % 4 == 2):
                newCords = [x, y + moveDist]
            else:
                newCords = [x + moveDist, y]
            return searchFromCords(img,newCords[0],newCords[1],boxLength, tolerance, numWanted, moveDist, direction)
        else:
            return searchFromCords(img,newCords[0],newCords[1],boxLength, tolerance, numWanted, moveDist, (direction + 1)%4)

#'''


#Open the video file
cap = cv2.VideoCapture('AzothVideo.mov')
print("Started")

stop = False
#Variable to stop the video

posAve = [62,68]
cords = [[900,775],[1025,915]]
while(cap.isOpened() and not(stop)):
    ret, pict = cap.read()
    #Read the video frame by frame while there is video to watch

    #display the frame
    cv2.namedWindow("pict", cv2.WINDOW_NORMAL)
    cv2.imshow("pict",pict)

    #900,775 (x,y)
    #1025,915 #Doesn't include

    realWorldPosAve = [cords[0][0] + posAve[0], cords[0][1] + posAve[1]]
    cords = [[realWorldPosAve[0] - 100,realWorldPosAve[1] - 200],[realWorldPosAve[0] + 100,realWorldPosAve[1] + 200]]

    #Goes (y,x) because row,collums swap
    #frame = pict[775:915,900:1025]
    frame = pict[cords[0][1]:cords[1][1],cords[0][0]:cords[1][0]]
    #print(frame)
    #print(frame[50,75])

    #frame = cv2.imread("AzothTest.png",1)

    boxLength = 5
    tolerance = 40
    numWanted = 100
    closeBoxes = []
    spotsChecked = []
    moveDist = 20
    direction = 0
    
    isCharacter = searchFromCords(frame, posAve[0],posAve[1], boxLength, tolerance, numWanted, moveDist, direction)

    #print("Is There a Character? " + str(isCharacter))

    if(isCharacter):
        posAve = np.array(np.mean(np.array(closeBoxes), axis = 0),dtype=int)

    #print(len(closeBoxes))
    #'''
    for box in closeBoxes:
        cv2.rectangle(frame, tuple([box[0]-1,box[1]-1]),tuple([box[0]+boxLength,box[1]+boxLength]), (0,255,0),1)
 

    for box in spotsChecked:
        cv2.rectangle(frame, tuple([box[0]-1,box[1]-1]),tuple([box[0]+1,box[1]+1]), (255,0,0),1)
    #'''
    cv2.rectangle(frame, tuple([posAve[0]-1,posAve[1]-1]),tuple([posAve[0]+1,posAve[1]+1]), (0,0,255),1)

    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.imshow("frame",frame)
    
    advance = False
    while(not(advance)):
        #Pause Each frame till space is presses
        k = cv2.waitKey(10)
        if k == ord(" "):
            advance = True
        elif k == 27:
            #If esc, ord(esc) == 27, is pressed end the programm
            advance = True
            stop = True

#Close the video and destroy windows
cap.release()
cv2.destroyAllWindows()
print("Done")
