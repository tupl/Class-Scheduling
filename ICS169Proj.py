import random
import math
import copy

import Class

import csv
with open('classroomData.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        print(row);

random.seed(0)  # repeatable random for problem generation
'''
numMajors = 10

classesPerMajor = 15

minClassSize = 10
maxClassSize = 100
'''
maxClassLength = 3 # largest consecutive number of time slots for a class

classes = []

with open('classroomData.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile)
    while(True):
        try:
            row1 = next(spamreader)
            print(row1)
            row2 = next(spamreader)
            print(row2)
            if not row1 or not row2:
                break
            for i in range(len(row1)):
                if i != 0 and row1[i] != '' and row2[i] != '': #header data
                    for count in range(int(row1[i])): # row1 contains the count of classes that are that size
                        classes.append(Class.Class(0, size = int(row2[i]), length = int(random.random() * maxClassLength)))
        except StopIteration:
            break
        '''
for major in range(numMajors):
    classes += [Class.Class(major, size = minClassSize + int(random.random() * (maxClassSize - minClassSize)), length = int(random.random() * maxClassLength)) for classNum in range(classesPerMajor)]
    '''
# NOTE: class length of zero is possible, and means that the class takes up no additional timeslots beyond the one it is assigned to
# (this makes things much easier to compute)

# classes that will be dropped because they don't fit into the schedule
droppedClasses = set(classes) #initialized to all classes because we start with an empty schedule

# pre Class-class classes
# classes = [[int(random.random() * maxClassSize) for _class in range(numMajorClasses)] for major in range(numMajors)]

numTimeSlots = 5

rooms = []

with open('roomData.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile)
    while(True):
        try:
            row1 = next(spamreader)
            print(row1)
            row2 = next(spamreader)
            print(row2)
            if not row1 or not row2:
                break
            for i in range(len(row1)):
                if i != 0 and row1[i] != '' and row2[i] != '': #header data
                    for count in range(int(row1[i])): # row1 contains the count of classrooms that are that soze
                        rooms.append(Class.Classroom(size = int(row2[i]), numTimeslots = numTimeSlots))
        except StopIteration:
            break
                
            
'''
numClassrooms = 50

minRoomSize = 10
maxRoomSize = 100

classNum = 0

rooms = [Class.Classroom(size = minRoomSize + int(random.random() * (maxRoomSize - minRoomSize)), numTimeslots = numTimeSlots) for room in range(numClassrooms)]
'''
# pre class rooms
# rooms = [int(random.random() * maxRoomSize) for room in range(numClassrooms)]

'''
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
'''

def printSchedule(schedule):
    for room in schedule:
        resultLine = "room size: " + repr(room.getSize()).rjust(3) + " : "
        lastRoom = "---"
        i = 0
        while(i < numTimeSlots):
            if(i in room.getClasses()):
                classSize = repr(room.getClass(i).getSize()).rjust(3)
                for index in range(room.getClass(i).getLength() + 1):
                    resultLine += " " + classSize
                    i += 1
            else:
                resultLine += " " + lastRoom
                i += 1
        print(resultLine)
            
def cost():  # minimize this
    result = 0

    for droppedClass in droppedClasses:
        result += droppedClass.getSize()
        
    for room in rooms:
        for key,Class in room.getClasses().items():
            overflow = (Class.getSize() - room.getSize()) * (Class.getLength() + 1)
            result += max(0, overflow) # add the number of students that don't fit, if any
    return result
    
    '''
    result = 0

    for droppedClass in droppedClasses:
        result += 10 * droppedClass.getSize()
        
    for room in rooms:
        for key,Class in room.getClasses().items():
            overflow = (Class.getSize() - room.getSize()) * Class.getLength()
            result += max(0, 5 * overflow) # add the number of students that don't fit, if any
            result += abs(min(0, overflow)) #add the amount of wasted space, if any
    return result'''

def numConflicts(): # meaningful objective function
    result = 0

    for droppedClass in droppedClasses:
        result += droppedClass.getSize()
        
    for room in rooms:
        for key,Class in room.getClasses().items():
            overflow = (Class.getSize() - room.getSize()) * Class.getLength()
            result += max(0, overflow) # add the number of students that don't fit, if any
    return result

    #pre class cost
    '''
    result = 0
    for slot in range(numTimeSlots):
        # conflicts = [[] for major in range(numMajors)] list of classes that cause time-slot conflicts for students
        for room in range(numClassrooms):
            result += max(0, classes[schedule[slot][room][0]][schedule[slot][room][1]] - rooms[room])  # if room isn't big enough, add the amount of students unable to fit
            # conflicts[schedule[slot][room][0]].append(classes[schedule[slot][room][0]][schedule[slot][room][1]])
        # for major in range(numMajors):
            # for i in range(len(conflicts[major])):
                # result += i * conflicts[major][i]  # adds the maximum amount of possible time-slot conflicts
    return result'''

currentCost = cost()  #cache the energy value


# initialize the global variables for currentMin
currentMin = currentCost
currentMinVector = copy.deepcopy(rooms)

def updateCurrentMin():
    global currentMin
    if(currentCost < currentMin):
        currentMin = currentCost
        # currentMinVector = copy.deepcopy(rooms)

temp = 5000
tempLoss = 0.999
cutoff = 0.1

# order in which to visit (is shuffled)
roomOrder = [i for i in range(len(rooms))]
timeSlotOrder = [i for i in range(numTimeSlots)]

random.seed()  # back to unrepeatable random

def process(room : Class.Classroom, timeSlot : int): # considers doing a modification
    global currentCost
    global rooms
    global droppedClasses
    global temp
    if(timeSlot in room.getClasses()): # if there is a room
        #try swapping it somewhere first
        removedClass = room.getClass(timeSlot)
        room.removeClass(timeSlot)
        
        targetRoomIndex = random.choice(range(len(rooms)))
        targetTimeSlot = random.choice(range(numTimeSlots))
        if(targetTimeSlot in rooms[targetRoomIndex].getClasses() and rooms[targetRoomIndex].getClass(targetTimeSlot).getLength() == removedClass.getLength()):
            # try swapping the classes
            room.addClass(timeSlot, rooms[targetRoomIndex].getClass(targetTimeSlot))
            rooms[targetRoomIndex].removeClass(targetTimeSlot)
            rooms[targetRoomIndex].addClass(targetTimeSlot, removedClass)
            newCost = cost()
            if(newCost < currentCost):
                # take it
                currentCost = newCost
                updateCurrentMin()
                return
            
            probability = math.pow(math.e, -(newCost - currentCost) / temp)
            if(random.random() > probability):
                # don't take it, so reset
                rooms[targetRoomIndex].removeClass(targetTimeSlot)
                rooms[targetRoomIndex].addClass(targetTimeSlot, room.getClass(timeSlot))
                room.removeClass(timeSlot)
            else: # take it
                currentCost = newCost
                updateCurrentMin()
                return
                

        elif(rooms[targetRoomIndex].canAddClass(targetTimeSlot, removedClass)):
            rooms[targetRoomIndex].addClass(targetTimeSlot, removedClass)
            newCost = cost()
            probability = math.pow(math.e, -(newCost - currentCost) / temp)
            if(random.random() > probability):
                # don't take it, so reset
                rooms[targetRoomIndex].removeClass(targetTimeSlot)
                
            else: #take it
                currentCost = newCost
                updateCurrentMin()
                return
            
        # try dropping the class next if the swap fails
        droppedClasses.add(removedClass)
        newCost = cost()
        probability = math.pow(math.e, -(newCost - currentCost) / temp)
        if(random.random() > probability):
            # don't take it, so reset
            room.addClass(timeSlot, removedClass)
            droppedClasses.remove(removedClass)
        else: #take it
            currentCost = newCost
            updateCurrentMin()
    else: #try adding a room
        if(len(droppedClasses) == 0):
            return
        addedClass = random.sample(droppedClasses, 1)[0]
        if(room.canAddClass(timeSlot, addedClass)):
            room.addClass(timeSlot, addedClass)
            droppedClasses.remove(addedClass)
            newCost = cost()
            probability = math.pow(math.e, -(newCost - currentCost) / temp)
            if(random.random() > probability):
                # don't take it, so reset
                room.removeClass(timeSlot)
                droppedClasses.add(addedClass)
            else: #take it
                currentCost = newCost
                updateCurrentMin()
            
        
        
#do SA
import time

t0 = time.time()

while(temp > cutoff):
    random.shuffle(roomOrder)

    for roomIndex in roomOrder:
        random.shuffle(timeSlotOrder)
        for timeSlot in timeSlotOrder:
            process(rooms[roomIndex], timeSlot)
    '''
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
                        '''
    # modify temp
    temp *= tempLoss

    # heartbeat
    # print(schedule)
    # printSchedule(rooms)
    print(currentCost, " : ", temp)

t1 = time.time()
printSchedule(rooms)
print(currentCost)
print("num conflicts: " + str(numConflicts()))
print("num dropped classes: " + str(len(droppedClasses)))
print("time: " + str(t1-t0))
for Class in droppedClasses:
    print(str(Class.getSize()) + " : " + str(Class.getLength()))


print("Lowest value reached (for debugging/testing):")

print(currentMin)

print("DONE!")
