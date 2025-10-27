# framework CRUD program

import json

MENUFILE = "menu.cfg"
FIELDFILE = "fields.cfg"
DATAFILE = "frameWorkRecords.dat"
DELETEDDATAFILE = "deletedRecords.dat"

def showMenu():
	while 1:
		printMenu()
		choice = int(input("Enter Your Choice: "))
		#operations = [create, showAll, update, delete, exit]
		#operations[choice - 1]()
		match choice:
			case 1:
				create()
			case 2:
				showAll()
			case 3:
				update()
			case 4:
				delete()
			case 5:
				print("Program Exited")
				exit(0)
			case _:
				print("Please Enter a Valid Choice!")

def create():
	readRecord()
	saveRecordsIntoFile()

def readRecord():
	"""for field in fields:
		fieldValue = input(f"Enter {field}: ")
		record.append(fieldValue)
	records.append(record)"""

	"""for fieldCounter in range(len(fields)):
		fieldValue = input(f"Enter {fields[fieldCounter]}: ")
		if (fieldCounter == (len(fields) - 1)):
			fieldValue = float(fieldValue)
		record.append(fieldValue)
	records.append(record)
	print("Saved Successfully!")"""

	record = []
	for counter, field in enumerate(fields):
		fieldValue = input(f"Enter {field}: ")
		if (counter == len(fields) - 1):
			fieldValue = float(fieldValue)
		record.append(fieldValue)
	records.append(record)
	print("Saved Successfully!")

def saveRecordsIntoFile():
	fpData = open(DATAFILE, "w")
	#fpData.write(str(records))
	json.dump(records, fpData)
	fpData.close()

def showAll():
	if (checkRecords()):
		return
	print("-----------")
	print("All records")
	print("-----------")
	for record in records:
		printRecord(record)

def printRecord(record):
	"""for record in records:  or #for recordCounter in range(len(records)):
		counter = 0
		for field in fields:
			#print(f"{field}: {records[recordCounter][counter]}")
			print(f"{field}: {record[counter]}")
			counter += 1 """
	for counter, field in enumerate(fields):
		print(f"{field}: {record[counter]}")

def update():
	if (checkRecords()):
		return
	tempRecord = searchRecord("Update")
	# print(id(tempRecord))
	if (tempRecord != None):
		tempRecord[len(fields) - 1] = float(input(f"Enter new {fields[len(fields) - 1]}: "))
		saveRecordsIntoFile()
		print(f"{fields[0]} {idToCheck} Updated Successfully!")
	else:
		print(f"{fields[0]} {idToCheck} is Not found!")

def searchRecord(operation):
	global idToCheck 
	idToCheck = input(f"Enter {fields[0]} to {operation}: ")
	for record in records:
		if (record[0] == idToCheck):
			#print(id(record))
			return record

def delete():
	if (checkRecords()):
		return
	tempRecord = searchRecord("Delete")
	if (tempRecord != None):
		#deletedRecords.append(tempRecord)
		saveDeletedIntoFile(tempRecord)
		records.remove(tempRecord)
		saveRecordsIntoFile()
		print(f"{fields[0]} {idToCheck} Deleted Successfully!")
	else:
		print(f"{fields[0]} {idToCheck} is Not Found!")

def saveDeletedIntoFile(tempRecord):
	fpDeleted = open(DELETEDDATAFILE, "a")
	fpDeleted.write(str(tempRecord))
	fpDeleted.close()

def printMenu():
	fpMenu = open(MENUFILE, "r")
	menu = fpMenu.read()
	if (not menu):
		print(f"{MENUFILE} is Empty!")
		fpMenu.close()
		return
	fpMenu.close()
	print(menu)

def loadFields():
	fpFields = open(FIELDFILE, "r")
	global fields 
	fields = fpFields.readlines()
	if (not fields):
		print(f"{FIELDFILE} is Empty!")
		fpFields.close()
		return 
	fpFields.close()
	for fieldCounter in range(len(fields) - 1):
		fields[fieldCounter] = fields[fieldCounter].strip()
	#print(fields)

def loadRecords():
	global records #without this it over writes in the empty globally declared variable
	fpData = open(DATAFILE, "r")
	content = fpData.read()
	# records = fpData.read() #reads as string. if readlines() is used then records are like list of string of list of list(["[[],[]]"])
	if (not content):
		records = []
		fpData.close()
		return
	records = json.loads(content)
	# records = eval(records) #changed to list of list
	fpData.close()
	# print(records) 

def checkRecords():
	if (not records):
		# print("No " + str(fields[0][:8]) + "Found!")
		print(f"No Records Found!") #records should be replaced by correct name like accounts, items, tickets. store it another .cfg and use it
		return 1

loadFields()
loadRecords()
showMenu()