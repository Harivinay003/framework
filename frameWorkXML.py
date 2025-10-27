# framework program data stored in xml format

import xml.etree.ElementTree as ET 

DATAFILE = "records.xml"
MENUFILE = "menu.cfg"
FIELDSFILE = "fieldsAndTags.xml"

# fields = ["Account Number", "Account Name", "Account Balance"]
# tags = ["Account_Number", "Account_Name", "Account_Balance"]

def showMenu():
	operations = [create, showAll, update, delete, exit]
	while 1:
		printMenu()
		choice = int(input("Enter Your Choice: "))
		operations[choice - 1]()

def printMenu():
	fpMenu = open(MENUFILE, "r")
	menu = fpMenu.read()
	fpMenu.close()
	print(menu)

def create():
	createRecord()
	saveRecordIntoFile()
	print("Saved Successfully!")

def createRecord():
	recordElement = ET.SubElement(root, "record")
	for counter, field in enumerate(fields):
		value = readValue(field)
		tagElement = ET.SubElement(recordElement, tags[counter])
		tagElement.text = value

def readValue(field):
	value = input(f"Enter {field}: ")
	return value

def saveRecordIntoFile():
	tree.write(DATAFILE)

def showAll():
	if (checkRecords()):
		return
	print("All Records")
	for recordElement in root.findall("record"):
		print("---------------")
		for counter, tag in enumerate(tags):
			element = recordElement.find(tag)
			print(f"{fields[counter]}: {element.text}")

def update():
	if (checkRecords()):
		return
	recordToUpdate = searchRecord("Update")
	# print(recordToUpdate)
	if (not recordToUpdate):
		print(f"{fields[0]} {idToCheck} Not Found!")
		return
	element = recordToUpdate.find(tags[-1])
	element.text = input(f"Enter New {fields[-1]}: ")
	saveRecordIntoFile()
	print(f"{fields[0]} {idToCheck} Updated Successfully")

def searchRecord(operation):
	global idToCheck
	idToCheck = input(f"Enter {fields[0]} to {operation}: ")
	for recordElement in root.findall("record"):
		element = recordElement.find(tags[0])
		if (idToCheck == element.text):
			# print(recordElement)
			return recordElement

def delete():
	if (checkRecords()):
		return
	recordToBeDeleted = searchRecord("Delete")
	if (not recordToBeDeleted):
		print(f"{fields[0]} {idToCheck} Not Found!")
		return
	root.remove(recordToBeDeleted)
	saveRecordIntoFile()
	print(f"{fields[0]} {idToCheck} Deleted Successfully")


def loadFieldsAndTags():
	global fields
	global tags 
	fields = []
	tags = []
	fieldTree = ET.parse(FIELDSFILE)
	rootForFields = fieldTree.getroot()
	subRoot = rootForFields.find("fields")
	fields = [element.text for element in subRoot.findall("field")]

	subRootForTags = rootForFields.find("tags")
	tags = [element.text for element in subRootForTags.findall("tag")]
	# print(tags)
	# print(fields)
	# for tag in tags:
	# 	element = root.find(tag)
	# 	fields.append(element.text)
	# print(fields)

def loadRecords():
	global tree
	global root
	try:
		tree = ET.parse(DATAFILE)
		root = tree.getroot()

	except ET.ParseError:
		root = ET.Element("records")
		tree = ET.ElementTree(root)
		# print(f"{DATAFILE} is Empty")

def checkRecords():
	if not root:
		print(f"{DATAFILE} is Empty!")
		return 1

loadFieldsAndTags()
loadRecords()
showMenu()