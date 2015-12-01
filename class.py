class Class:
	id = 0; # static ID counter 
	def __init__(self, major, size, length):
		self.major = major
		self.size = size
		self.length = length
		self.id = Class.id
		Class.id = Class.id + 1

	def setLocation(self, location):
		# This one should save the location
		# of the classroom
		self.location = location

	def setTimeSlot(self, timeslot):
		self.timeslot = timeslot

	def getLocation(self):
		return self.location

	def getTimeSlot(self):
		return self.timeslot

	'''def setID(self, id):
		self.id = id'''

	def setMajor(self, major):
		self.major = major

	def setSize(self, size):
		self.size = size

	def selfLength(self, length):
		self.length = length

	def getID(self):
		return self.id

	def getMajor(self):
		return self.major

	def getSize(self):
		# how many student of this class
		return self.size

	def getLength(self):
		# how long is this class
		return self.length

class Classroom:
	'''
		For each classroom, it will contains all class
			and its timeslot
		I suggest that we make a dictionary that
			map timeslot -> class
	'''

	id = 0; # static ID counter

	def __init__(self, size, numTimeslots):
		self.size = size
		self.numTimeslots = numTimeslots
		self.id = id
		Classroom.id = Classroom.id + 1
		self.timeslots = {}

	def addClass(self, timeslot, Class):
		self.timeslots[timeslot] = Class

	def canAddClass(self, timeslot, Class) -> bool:
		classEnd = timeslot + Class.getLength()
		if(classEnd >= self.numTimeslots):
			return False # timeslot extends off of the end
		
		for slot in self.timeslots.keys():
			previousClassEnd = slot + self.timeslots[slot].getLength()
			if(slot <= classEnd and previousClassEnd >= classEnd):
				#the end of the class overlaps
				return False
			if(timeslot <= previousClassEnd and timeslot >= slot):
				#the begin of the class overlaps
				return False
			if(timeslot >= slot and classEnd <= previousClassEnd):
				#class is inside an existing class
				return False
		# no problems
		return True

	def getClass(self, timeslot):
		return self.timeslots[timeslot]

	def getClasses(self) -> {}:
		return self.timeslots

	def removeClass(self, timeslot):
		del(self.timeslots[timeslot])

	def getSize(self):
		return self.size

	def getID(self):
		return self.id

	def setSize(self, size):
		self.size = size

	'''def setID(self, id):
		self.id = id'''
