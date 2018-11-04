import sys
import time
import math
from tkinter import *
lineBrk = "-" * 64
wid = 1280
hi = 720
master = Tk()
img = PhotoImage(file="merica.gif")
us = Canvas(master,width=wid,height=hi)
us.create_image(640,360,image = img)
us.pack()

xMin = 14.68673
yMin = -130.35722
xMax = 60.84682
yMax = -60.02403

xFactor = hi/(xMax - xMin);
yFactor = wid/(yMax - yMin);


	
def path(start, goal, closedSet):
	#print("Building Path")
	current = goal
	solution = list()
	prev = ""
	while current != "":
		if prev != "":
			line(current,prev,"green",True,4)
		solution.append(current)
		prev = current
		current = closedSet[current]
	return cleanData(solution[::-1])
def data(start, elapsed, sequence, length):
        global lineBrk
        print("Found Solution")
        print("Total Distance: " + str(length) + " miles")
        print("Number of Stations: " + str(len(sequence)))
        string = str(str(int(length)) + " miles, " + str(len(sequence)) + " stations in ~" + str(int(length/100)) + " hrs")
        txt = Label(master, text = string, justify = 'center', font = ("Courier", 20), pady = 4)
        txt.pack()
        print(lineBrk)
        return
def getNbrs(station):
	nbrs = list()
	for item in stationDict[station]:
		nbrs.append(item)
	#print(station + ": " + str(nbrs))
	return nbrs
def getDist(one, two):
	x1 = locationsDict[one][0]
	y1 = locationsDict[one][1]
	x2 = locationsDict[two][0]
	y2 = locationsDict[two][1]
	return calcd(y1,x1,y2,x2)
def cleanData(solution):
	for i in range(len(solution)):
		if solution[i] in node2name:
			solution[i] = node2name[solution[i]]
	return solution
def line(one, two, color, up, wide):
	global xMin,xMax,yMin,yMax,xFactor,yFactor
	global us, master, wid, hi
	y1 = (float(locationsDict[one][1])  - xMin)*xFactor
	y2 = (float(locationsDict[two][1]) - xMin)*xFactor
	x1 = (yMax - float(locationsDict[one][0]))*yFactor
	x2 = (yMax - float(locationsDict[two][0]))*yFactor
	x1 = abs(x1)
	x2 = abs(x2)
	y1 = abs(y1)
	y2 = abs(y2)
	widMid = wid/2
	hiMid = hi/2
	if x1 > widMid:
		x1 = widMid - (x1-widMid)
	else:
		x1 = widMid + (widMid - x1)
	if x2 > widMid:
		x2 = widMid - (x2-widMid)
	else:
		x2 = widMid + (widMid - x2)

	if y1 > hiMid:
		y1 = hiMid - (y1-hiMid)
	else:
		y1 = hiMid + (hiMid - y1)
	if y2 > hiMid:
		y2 = hiMid - (y2-hiMid)
	else:
		y2 = hiMid + (hiMid - y2)
	#coords = [x1,y1,x2,y2]
	#print(coords)
	us.create_line(x1,y1,x2,y2,fill=color, width=wide)
	#us.create_line(0,0,250,250,fill=color, width=1)
	us.pack()
	if up:
		master.update()
	return

def aStar(start,goal):
	global master
	count = 0
	startTime = time.time()
	if start == goal:
		data(start,time.time()-start,[start])
		return
	openSet = list()
	closedSet = dict()
	prevEst = getDist(start, goal)
	openSet.append((prevEst,0,start,""))
	print("Starting A-Star: " + start + " | " + goal)
	#print(openSet)
	while openSet:
		count+=1
		if count % 50 == 0:
			master.update()
		openSet.sort()
		#print(openSet)
		curr = openSet.pop(0)
		if curr[2] in closedSet:
			continue
		closedSet[curr[2]] = curr[3]
		if curr[3] != "":
			line(curr[2],curr[3],"cyan",False,2)
		if curr[2] == goal:
			print("openSet: " + str(len(openSet)))
			print("closedSet: " + str(len(closedSet)))
			data(start, time.time()-startTime, path(start, goal, closedSet), curr[1])
			return
		
		prevEst = curr[0]
		nextLayer = getNbrs(curr[2])
		#print(nextLayer)
		for nbr in nextLayer:
			if nbr[0] in closedSet:
				continue
			gap = nbr[1]
			newEst = curr[1] + gap + getDist(nbr[0], goal)
			openSet.append((newEst, curr[1] + gap, nbr[0], curr[2]))
			line(curr[2],nbr[0],"red",False,1)
			


def calcd(y1,x1,y2,x2):
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # if (and only if) the input is strings
   # use the following conversions
	
	y1  = float(y1)
	x1  = float(x1)
	y2  = float(y2)
	x2  = float(x2)
	
	R   = 3958.76 # miles = 6371 km
	y1 *= abs(math.pi/180.0)
	x1 *= abs(math.pi/180.0)
	y2 *= abs(math.pi/180.0)
	x2 *= abs(math.pi/180.0)
	return math.acos(abs(math.sin(y1)*math.sin(y2) + math.cos(y1)*math.cos(y2)*math.cos(x2-x1) )) * R


input = sys.argv;

stationFile = open("rrEdges.txt", 'r')
namesFile = open("rrNodeCity.txt", 'r')
locationFile = open("rrNodes.txt", 'r')
stations = stationFile.readlines()
names = namesFile.readlines()
locations = locationFile.readlines()

stationDict = dict()
namesDict = dict()
locationsDict = dict()
node2name = dict()
#xCoords = list()
#yCoords = list()
if True:
	for item in locations:
		space = item.find(' ')
		space2 = len(item)-1-item[::-1].find(' ')
		name = str(item[:space])
		x = str(item[space+1:space2])
		#xCoords.append(float(x))
		y = str(item[space2+1:len(item)-1])
		#yCoords.append(float(y))
		locationsDict[name] = (y,x)
	for item in stations:
		space = item.find(' ')
		name = str(item[:space])
		nbr = str(item[space+1:len(item)-1])
		if name not in stationDict.keys():
			stationDict[name] = list()
		if nbr not in stationDict.keys():
			stationDict[nbr] = list()
		stationDict[name].append(nbr)
		stationDict[nbr].append(name)
	for item in names:
		space = item.find(' ')
		node = str(item[:space])
		name = str(item[space+1:len(item)-1])
		namesDict[name] = node
		node2name[node] = name
	for item in stationDict:
		nbrs = stationDict[item]
		stationDict[item] = list()
		x1 = locationsDict[item][0]
		y1 = locationsDict[item][1]
		for nbr in nbrs:
			x2 = locationsDict[nbr][0]
			y2 = locationsDict[nbr][1]
			stationDict[item].append((nbr,calcd(y1,x1,y2,x2)))


#print(getDist(namesDict["Miami"], namesDict["Orlando"]))
#exit()

count = 1
for item in stationDict.keys():
	for item2 in stationDict[item]:
		line(item,item2[0],"black",False,1)
		count+=1
		if count % 500 == 0:
			master.update()
startingCity = ""
endingCity = ""
eS = Entry(master)
eS.insert(0, "Starting City")
eS.bind("<FocusIn>", lambda args: eS.delete('0', 'end'))
eS.pack()
eF = Entry(master)
eF.insert(0, "Ending City")
eF.bind("<FocusIn>", lambda args: eF.delete('0', 'end'))
eF.pack()

us.create_line(0,720,1280,720,fill = 'black', width = 1)
us.pack()

def getStartInput():
        startingCity = eS.get()
        endingCity = eF.get()
        print(startingCity)
        print(endingCity)
        if '0' not in startingCity:
                startingCity = namesDict[startingCity]
        if '0' not in endingCity:
                endingCity = namesDict[endingCity]
        line(startingCity,endingCity,"yellow", True,4)
        aStar(startingCity,endingCity)
        mainloop()
        exit()

bS = Button(master, text="GO!", width=10, command=getStartInput)
bS.pack()

mainloop()

e = Entry(master, width=50)
e.pack()

text = e.get()

def makeentry(parent, caption, width=None, **options):
    Label(parent, text=caption).pack(side=LEFT)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack(side=LEFT)
    return entry

start = makeentry(parent, "Starting: ", 10)
finish = makeentry(parent, "Ending: ", 10)

content = StringVar()
entry = Entry(parent, text=caption, textvariable=content)

text = content.get()
content.set(text)


if len(input) == 4:
	if input[1] in ["San", "Ciudad", "Los", "Las", "St"]:
		startingCity = str(input[1] + " " + input[2])
		endingCity = input[3]
	if input[2] in ["City", "DC"]:
		startingCity = str(input[1] + " " + input[2])
		endingCity = input[3]
	if input[2] in ["San", "Ciudad", "Los", "Las", "St"]:
		startingCity = input[1]
		endingCity = str(input[2] + " " + input[3])
	if input[3] in ["City", "DC"]:
		startingCity = input[1]
		endingCity = str(input[2] + " " + input[3])
elif len(input) == 5:
	startingCity = str(input[1] + " " + input[2])
	endingCity = str(input[3] + " " + input[4])
else:
	startingCity = input[1]
	endingCity = input[2]
if '0' not in startingCity:
	startingCity = namesDict[startingCity]
if '0' not in endingCity:
	endingCity = namesDict[endingCity]
print(locationsDict[startingCity])
print(locationsDict[endingCity])
line(startingCity,endingCity,"yellow", True,4)
aStar(startingCity,endingCity)
mainloop()
exit()
