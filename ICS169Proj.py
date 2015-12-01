import random
import math
import copy

import Class

random.seed(0)  # repeatable random for problem generation

numMajors = 10

classesPerMajor = 10

maxClassSize = 100

maxClassLength = 3 # largest consecutive number of time slots for a class

classes = []
for major in range(numMajors):
    classes += [Class.Class(major, size = int(random.random() * maxClassSize), length = int(random.random() * maxClassLength)) for classNum in range(classesPerMajor)]
# NOTE: class length of zero is possible, and means that the class takes up no additional timeslots beyond the one it is assigned to
# (this makes things much easier to compute)

# classes that will be dropped because they don't fit into the schedule
droppedClasses = set(classes) #initialized to all classes because we start with an empty schedule

# pre Class-class classes
# classes = [[int(random.random() * maxClassSize) for _class in range(numMajorClasses)] for major in range(numMajors)]

numTimeSlots = 5

numClassrooms = 60

maxRoomSize = 100

classNum = 0

rooms = [Class.Classroom(size = int(random.random() * maxClassSize), numTimeslots = numTimeSlots) for room in range(numClassrooms)]

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
        resultLine = "room size: " + repr(room.getSize()).rjust(3)
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
            result += max(0, (Class.getSize() - room.getSize()) * Class.getLength()) # add the number of students that don't fit, if any

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
        currentMinVector = copy.deepcopy(rooms)

temp = 5000
tempLoss = 0.995
cutoff = 0.5

# order in which to visit (is shuffled)
roomOrder = [i for i in range(len(rooms))]
timeSlotOrder = [i for i in range(numTimeSlots)]

random.seed()  # back to unrepeatable random

def process(room : Class.Classroom, timeSlot : int): # considers doing a modification
    global currentCost
    if(timeSlot in room.getClasses()): # if there is a room we can delete
        removedClass = room.getClass(timeSlot)
        room.removeClass(timeSlot)
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
    print(currentCost)
    
printSchedule(rooms)
print(currentCost)


print("Lowest value reached (for debugging/testing):")

printSchedule(currentMinVector)
print(currentMin)

print("DONE!")

