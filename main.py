import random

#reads data from the file Rooms and returns a list of courses
def readCourses():
    courses = []
    with open('Exam Details/Courses') as file:
        for line in file:
            courses.append(line.strip())
    return courses

#reads data from the file Rooms and returns a list of rooms
def readRooms():
    rooms = []
    with open('Exam Details/Rooms') as file:
        for line in file:
            rooms.append(line.strip())
    return rooms


#reads Data from the file Time Slots and returns a list of time slots
def readSlots():
    timeSlots = []
    with open('Exam Details/Time Slots') as file:
        for line in file:
            timeSlots.append(line.strip())
    return timeSlots


#reads data from the file registations and returns a list of tuples of the form (student,course)
def readRegistrations():
    registrations = []
    with open('Exam Details/Registrations') as file:
        for line in file:
            oneLine = line.strip().split(',')
            tup = (oneLine[0],oneLine[1])
            registrations.append(tup)
    return registrations


#creates a list of all the possible combinations of courses,rooms and timeSlots
def initiate(courses,rooms,timeSlots):
    possibleCombinations = []
    for course in courses:
        courseCol = []
        for room in rooms:
            for timeSlot in timeSlots:
                courseCol.append((course,room,timeSlot))
        random.shuffle(courseCol)
        possibleCombinations.append(courseCol)
    return possibleCombinations

#creates the initial population
def initialPopulation(dataSet):
    possibilitiesOfEachCourse = len(dataSet[0])
    population = []
    for i in range(possibilitiesOfEachCourse):
        chromosome = []
        for course in dataSet:
            chromosome.append(course[i])
        population.append(chromosome)
    return population


#Creates random tuple for a course in the chromosome
def randomRoomTimeSlot(chromosome,rooms,timeSlots,j):
    #randomly select a room and time slot for a course
    tempList = list(chromosome[j])
    tempList[1] = random.choice(rooms)
    tempList[2] = random.choice(timeSlots)
    chromosome[j] = tuple(tempList)
    return chromosome[j]


#checks wheather the chromosome is valid or not (not using the same room at the same time for two courses)
def Validify(chromosome,registrations,rooms,timeSlots):
    #check if the chromosome is valid
    for i in range(len(chromosome)):
        for j in range(i+1,len(chromosome)):
            if chromosome[i][1] == chromosome[j][1] and chromosome[i][2] == chromosome[j][2]:
                chromosome[j] = randomRoomTimeSlot(chromosome,rooms,timeSlots,j)
                Validify(chromosome,registrations,rooms,timeSlots)
    return chromosome


#performs single point crossover for two chromosomes
def singlePointCrossover(chromosome1,chromosome2):
    point = random.randint(0,len(chromosome1)-1)
    temp = chromosome1[point:]
    chromosome1[point:] = chromosome2[point:]
    chromosome2[point:] = temp
    return chromosome1,chromosome2

#mutates a chromosome by adding a random room and time slot to a course
def mutation(chromosome,rooms,timeSlots):
    point = random.randint(0,len(chromosome)-1)
    chromosome[point] = randomRoomTimeSlot(chromosome,rooms,timeSlots,point)
    return chromosome


#makes a list of possible clashes between courses (clashing students)
#and a list of tuples of the form (course1,course2,clashing students)
def clashes(registrations,courses):
    clashes = []
    clashesCount =[]
    for i in range(len(courses)):
        for j in range(i+1,len(courses)):
            clashes.append((courses[i],courses[j]))
            clashesCount.append((courses[i],courses[j],0))
    studentCourses = []
    lastChecked = ''
    index = 0
    for i in range(len(registrations)):
      if registrations[i][0] != lastChecked:
        studentCourses.append([])
        student = registrations[i][0]
        lastChecked = student
        for registration in registrations:
            if registration[0] == student:
                studentCourses[index].append(registration[1])
        index += 1
    for student in studentCourses:
        for i in range(len(student)):
            for j in range(i+1,len(student)):
                if (student[i],student[j]) in clashes:
                    ind = clashes.index((student[i],student[j]))
                    clashesCount[ind] = (clashes[ind][0],clashes[ind][1],clashesCount[ind][2]+1)
                elif (student[j],student[i]) in clashes:
                    ind = clashes.index((student[j],student[i]))
                    clashesCount[ind] = (clashes[ind][0],clashes[ind][1],clashesCount[ind][2]+1)
    return clashesCount,clashes


#calculates the fitness of a chromosome (10 points for clashes and 1 point for using the same room at the same time)
def fitness(chromosome,clashesCount,clashes):
    fitness = 0
    #makes sure that no two courses are held in the same room at the same time
    for i in range(len(chromosome)):
        for j in range(i+1,len(chromosome)):
            if chromosome[i][1] == chromosome[j][1] and chromosome[i][2] == chromosome[j][2]:
                fitness += 1
    #makes sure not two courses with a clash are held at the same time
    for i in range(len(clashes)):
        c1 = clashes[i][0]
        c2 = clashes[i][1]
        for j in range(len(chromosome)):
            if chromosome[j][0] == c1:
                time = chromosome[j][2]
                for k in range(j+1,len(chromosome)):
                    if chromosome[k][0] == c2 and chromosome[k][2] == time:
                        fitness += (clashesCount[i][2]*(10))
            elif chromosome[j][0] == c2:
                time = chromosome[j][2]
                for k in range(j+1,len(chromosome)):
                    if chromosome[k][0] == c1 and chromosome[k][2] == time:
                        fitness += (clashesCount[i][2]*(10))
    return fitness

#main function
if __name__ == '__main__':
    #File Reading
    courses = readCourses()
    rooms = readRooms()
    timeSlots = readSlots()
    registrations = readRegistrations()

    #Pre-processing
    dataSet = initiate(courses,rooms,timeSlots)
    population = initialPopulation(dataSet)
    corrected = []
    clashCount,clashes = clashes(registrations,courses)

    #validating chromosomes
    for chromosome in population:
        corrected.append(Validify(chromosome,registrations,rooms,timeSlots))

    #variable initiation
    best = None
    flag = False
    bestScore = -1
    itc = -1

    #actual Algorithm
    for i in range(10000):
        rankSolutions = []
        for chromosome in corrected:
            rankSolutions.append( ( chromosome, fitness(chromosome,clashCount,clashes) ) )
            if best == None or fitness(chromosome,clashCount,clashes) < bestScore:
                best = chromosome
                itc = i
                bestScore = fitness(chromosome,clashCount,clashes)
            if bestScore == 0:
                print(best," is the best solution with zero clashes")
                flag = True
                break
        rankSolutions.sort(key=lambda x: x[1])
        select = []
        for j in range(len(rankSolutions)//2):
                select.append(rankSolutions[j][0])
        newGeneration = []
        for k in range(len(select)):
            child1,child2 =None,None
            if random.randint(0,100) < 80:
                child1,child2 = singlePointCrossover(select[k],select[random.randint(0,len(select)-1)])
            else:
                child1 = mutation(select[k],rooms,timeSlots)
                child2 = mutation(select[random.randint(0,len(select)-1)],rooms,timeSlots)
            newGeneration.append(child1)
            newGeneration.append(child2)
        correctedNewgen = []
        for chromosome in newGeneration:
            correctedNewgen.append(Validify(chromosome,registrations,rooms,timeSlots))
        corrected = correctedNewgen
        if flag:
            break
    if not flag:
        print(best, " is the best solution founded in 10000 iterations with ",bestScore," conflict score (",int(bestScore/10),") clashes. Increase timeslots or rooms to reduce the number of clashes.")





