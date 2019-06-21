import cv2
import numpy as np
import time
#import math

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

    #print("Spot:" + str([x,y]) + ": " + str(img[x,y]))

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
            
            
dave = cv2.imread("AzothTest.png",1)

timesArray = []

spotsChecked = []

#Self Explanitory Variable
boxLength = 5
#How close each of the pixels have to be. Pretty high number
tolerance = 30
#Number of similar boxes to be considered that this clump of pixels is the character
numWanted = 50

moveDist = 20

#0 = Up, 1 = Left, 2 = Down, 3 = Right
direction = 0 

#for i in range(0,1000):

startTime = time.time()

#Make a variable that stores which boxes have been deemed close
#It is out here and not in the search From Cords method because it needs to be accessable by all methods
closeBoxes = []

#isCharacter = searchFromCords(dave, 10, 10, boxLength, tolerance, numWanted, moveDist, direction)


#Error. Must Fix
#Seems to be happening when I try to pas into (1,1)....
#isCharacter = searchFromCords(dave, 1, 1, boxLength, tolerance, numWanted, moveDist, direction)
#isCharacter = searchFromCords(dave, 21, 21, boxLength, tolerance, numWanted, moveDist, direction)
#isCharacter = searchFromCords(dave, -19, -19, boxLength, tolerance, numWanted, moveDist, direction)


#That error isn't with negatives...
#But there is another one where negative coordinates are validated.
#isCharacter = searchFromCords(dave, -10, -10, boxLength, tolerance, numWanted, moveDist, direction)

#NeverMind, -1 & -2 don't work
#isCharacter = searchFromCords(dave, -2, -2, boxLength, tolerance, numWanted, moveDist, direction)
#These errors dont crash the program so we are good for now.

isCharacter = searchFromCords(dave, 2, 2, boxLength, tolerance, numWanted, moveDist, direction)

#print("SIZE: " + str(dave.shape))
#(190, 239, 3)

endTime = time.time()

print("Is There a Character? " + str(isCharacter))
#print(closeBoxes)

if(isCharacter):
    #Get the average of the close boxes and cast it as an int.
    posAve = np.array(np.mean(np.array(closeBoxes), axis = 0),dtype=int)
    #print(posAve)
    #print(closeBoxes)
     

timesArray.append(endTime - startTime)
print("Time for average: " + str(timesArray[-1]))

print(len(closeBoxes))
for box in closeBoxes:
    if(closeBoxes.index(box) < 1):
        print(dave[-18,-78])
        print(dave[dave.shape[0] - 18, dave.shape[1] - 78])
        #print(dave[-68,70])
    cv2.rectangle(dave, tuple([box[0]-1,box[1]-1]),tuple([box[0]+boxLength,box[1]+boxLength]), (0,255,0),1)
    #print([box[0]-1,box[1]-1])

for box in spotsChecked:
    cv2.rectangle(dave, tuple([box[0]-1,box[1]-1]),tuple([box[0]+1,box[1]+1]), (255,0,0),1)
    #print(box)

cv2.rectangle(dave, tuple([posAve[0]-1,posAve[1]-1]),tuple([posAve[0]+1,posAve[1]+1]), (0,0,255),1)
   
#First Tests: SUCCESSS! 1000 times average without prints = 0.002666617155075073
#print("AVERAGEEEE: " + str(np.mean(np.array(timesArray))))

cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.imshow("frame", dave)

cv2.waitKey(0)
cv2.destroyAllWindows()
print("DONE")
