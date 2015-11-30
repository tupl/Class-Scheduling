import random
import math
import copy

import Class

random.seed(0)  # repeatable random for problem generation

numMajors = 3

numMajorClasses = 10

maxClassSize = 100

classes = [[int(random.random() * maxClassSize) for _class in range(numMajorClasses)] for major in range(numMajors)]

numTimeSlots = 5

numClassrooms = 6

maxRoomSize = 100

classNum = 0

rooms = [int(random.random() * maxRoomSize) for room in range(numClassrooms)]


def getNextClass(classNum : int):
    result = (classNum // numMajorClasses, classNum % numMajorClasses)
    return result

schedule = [[ getNextClass(slot * numClassrooms + room) for room in range(numClassrooms)] for slot in range(numTimeSlots)]
# (major No., class No.)

def printSchedule(schedule : [[(int, int)]]):
    moddableSchedule = copy.deepcopy(schedule)
    for slot in range(len(schedule)):
        for room in range(len(schedule[slot])):
            moddableSchedule[slot][room] = (str(moddableSchedule[slot][room][0]).zfill(2), str(classes[schedule[slot][room][0]][schedule[slot][room][1]]).zfill(2)) # replace class number with the number of people in that class
    print(moddableSchedule)

def cost():  # minimize this
    result = 0
    for slot in range(numTimeSlots):
        conflicts = [[] for major in range(numMajors)]
        for room in range(numClassrooms):
            result += max(0, classes[schedule[slot][room][0]][schedule[slot][room][1]] - rooms[room])  # if room isn't big enough
            conflicts[schedule[slot][room][0]].append(classes[schedule[slot][room][0]][schedule[slot][room][1]])
        for major in range(numMajors):
            for i in range(len(conflicts[major])):
                result += i * conflicts[major][i]  # if classes conflict
    return result

def swap(a : (int, int), b : (int, int)):
    temp = schedule[a[0]][a[1]]
    schedule[a[0]][a[1]] = schedule[b[0]][b[1]]
    schedule[b[0]][b[1]] = temp

currentCost = cost()  #cache the energy value

currentMin = currentCost
currentMinVector = schedule[:]

temp = 1000
tempLoss = 0.99
cutoff = 0.2

slotOrder1 = [i for i in range(numTimeSlots)]  # order in which we will visit timeslots
slotOrder2 = [i for i in range(numTimeSlots)]
roomOrder1 = [i for i in range(numClassrooms)]
roomOrder2 = [i for i in range(numClassrooms)]

random.seed()  # back to unrepeatable random

while(temp > cutoff):
    random.shuffle(slotOrder1)
    random.shuffle(slotOrder2)
    random.shuffle(roomOrder1)
    random.shuffle(roomOrder2) 
    for slotIndex in range(numTimeSlots):
        for roomIndex in range(numClassrooms):
            swap((slotOrder1[slotIndex], roomOrder1[roomIndex]), (slotOrder2[slotIndex], roomOrder2[roomIndex]))
            newCost = cost()
            if(newCost < currentCost):
                currentCost = newCost  #take it
                if(currentCost < currentMin):
                    currentMin = currentCost
                    currentMinVector = copy.deepcopy(schedule)
            else:
                # newCost > oldCost
                probability = math.pow(math.e, -(newCost - currentCost) / temp)
                if(random.random() > probability):
                    # don't take it, so reset
                    swap((slotOrder1[slotIndex], roomOrder1[roomIndex]), (slotOrder2[slotIndex], roomOrder2[roomIndex]))
                else:
                    currentCost = newCost  # take it
                    if(currentCost < currentMin):
                        currentMin = currentCost
                        currentMinVector = copy.deepcopy(schedule)
    # modify temp
    temp *= tempLoss

    # heartbeat
    print(schedule)
    print(currentCost)
    
printSchedule(schedule)
print(currentCost)

print(rooms)

print("Lowest value reached (for debugging/testing):")

printSchedule(currentMinVector)
print(currentMin)

print("DONE!")

