**GROUP MEMBERS**
Derek Alexander Edrich
Dylan Cockerham
Rodrigo Hernandez
Tu Le Phu Hoang

**OVERVIEW**
- 	The file "ClassSchedulerFeasibleRunTime" generates random classes/timeslots.
NOTE: runtime ~3 minutes.

- 	The file ICS169Proj.py file was the one that uses all classes/classrooms in the 2016 Winter Quarter for UCI.
NOTE: runtime is ~160 minutes.

**ZIP FILE CONTENTS**
-   "ClassSchedulerFeasibleRunTime.py" is our class scheduler that uses a smaller number of 
	randomly generated classes/classrooms.
	
- 	"ICS169Pro.py" is our final class scheduler.

- 	Input files are classroomData and roomData, which have the information for the classes and classroom 
	data, respectively.
	
- 	There are two classroomData files, one easier to edit, and one as a .csv file, so that it is easier 
	for Python to read.
	
- classScheduleResults.txt is the class schedule in text form after running "ICS169Proj.py".


**READING THE CLASS SCHEDULE**
The column on the left specifies the length of the room, and each subsequent column is a time slot.
Numbers in these columns represents the number of students in the class that takes up the time slot 
it is in.
A "---" means that no class is assigned to that particular room in the time slot.

EXAMPLE:
room size:  30 :  ---  30  30 ---  10 --- ---  30 --- ---  20  20  20  20  20 ---
means a room with size 30 is assigned no class in timeslot 1, a class of 30 in timeslot 2, a class of 30 in timeslot 3, and so on.


