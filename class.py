class Class:
	def __init__(self, major, size, length, id):
		self.major = major
		self.size = size
		self.length = length
		self.id = id

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

	def setID(self, id):
		self.id = id

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

	def __init__(self, size, id):
		self.size = size
		self.id = id
		self.timeslots = {}

	def addClass(self, timeslot, class):
		self.timeslots[timeslot] = class

	def getClass(self, timeslot):
		return self.timeslots[timeslot]

	def getSize(self):
		return self.size

	def getID(self):
		return self.id

	def setSize(self, size):
		self.size = size

	def setID(self, id):
		self.id = id