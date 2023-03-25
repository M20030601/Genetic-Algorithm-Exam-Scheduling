
numCourses = int(input("How many courses do you want to generate? "))
numRooms = int(input("How many rooms do you want to generate? "))
numTimeSlots = int(input("How many time slots do you want to generate? "))

Courses = []
Rooms = []
TimeSlots = []

for i in range(numCourses):
    Courses.append("C" + str(i+1))
for i in range(numRooms):
    Rooms.append("R" + str(i+1))
for i in range(numTimeSlots):
    TimeSlots.append("T" + str(i+1))

Registrations = []
for i in range(numCourses):
    for j in range(i+1,numCourses):
        clashes = int(input("clashes in " + Courses[i] + " and " + Courses[j] + "? "))
        for k in range(clashes):
            Registrations.append("S"+str(k+1)+","+Courses[i])
            Registrations.append("S"+str(k+1)+","+Courses[j])

print(Registrations)
with open('Exam/Courses', 'w') as file:
    for course in Courses:
        file.write(course + "\n")
with open('Exam/Rooms', 'w') as file:
    for room in Rooms:
        file.write(room + "\n")
with open('Exam/Time Slots', 'w') as file:
    for timeSlot in TimeSlots:
        file.write(timeSlot + "\n")
with open('Exam/Registrations', 'w') as file:
    for registration in Registrations:
        file.write(registration + "\n")



