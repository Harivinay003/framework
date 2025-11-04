#frameWork program using SQLite - database

import sqlite3

DATAFILE = "records.db"
MENUFILE = "menu.cfg"

class CRUD:
	def __init__(self):
		self.connectDb(DATAFILE)
		self.tableName = self.getFirstTableName()
		self.fields = self.getFieldsFromTable(self.tableName)
		self.getMenu()

	def create(self):
		record = self.readRecordFromUser()
		self.saveRecordIntoDatabase(record)

	def readRecordFromUser(self):
		record = []
		for counter, field in enumerate(self.fields):
			fieldValue = input(f"Enter {field}: ")
			if (counter == len(self.fields) - 1):
				fieldValue = float(fieldValue)
			record.append(fieldValue)
		return record

	def saveRecordIntoDatabase(self, record):
		try:
			self.cursor.execute(f"INSERT INTO {self.tableName} VALUES ({','.join(['?'] * len(record))})", record)
			self.commit()
			self.printSuccessfulMessage(record[0], "Saved")
		except sqlite3.IntegrityError:
			print(f"{self.fields[0]} already exists!")
		
	def showAll(self):
		if (self.checkRecords()):
			return
		self.cursor.execute(f"SELECT * FROM {self.tableName}")
		records = self.cursor.fetchall()
		print("\nAll Records\n------------")
		for record in records:
			self.printRecord(record)

	def printRecord(self, record):	
		for counter, field in enumerate(self.fields):
			print(f"{field}: {record[counter]}")

	def update(self):
		if (self.checkRecords()):
			return
		recordToBeUpdated, idToCheck = self.searchRecord("Update")
		if (not recordToBeUpdated):
			self.printNotFoundMessage(idToCheck)
			return
		newValue = float(input(f"Enter New {self.fields[-1]}: "))
		self.cursor.execute(f'UPDATE {self.tableName} SET "{self.fields[-1]}" = ? WHERE "{self.fields[0]}" = ?', (newValue, idToCheck))
		self.commit()
		self.printSuccessfulMessage(idToCheck, "Updated")

	def searchRecord(self, operation):
		idToCheck = input(f"Enter {self.fields[0]} to {operation}: ")
		self.cursor.execute(f'SELECT * FROM {self.tableName} WHERE "{self.fields[0]}" = ?', (idToCheck,))
		record = self.cursor.fetchone()
		return record, idToCheck

	def delete(self):
		if (self.checkRecords()):
			return
		recordToBeDeleted, idToCheck = self.searchRecord("Delete")
		if (not recordToBeDeleted):
			self.printNotFoundMessage(idToCheck)
			return
		self.cursor.execute(f'DELETE FROM {self.tableName} WHERE "{self.fields[0]}" = ?', (idToCheck,))
		self.commit()
		self.printSuccessfulMessage(idToCheck, "Deleted")

	def printNotFoundMessage(self, idNumber):
		print(f"{idNumber} Not Found!")

	def printSuccessfulMessage(self, idNumber, operation):
		print(f"{self.fields[0]} {idNumber} {operation} Successfully!")

	def connectDb(self, dataFile):
		self.connection = sqlite3.connect(dataFile)
		self.cursor = self.connection.cursor()
		
	def commit(self):
		self.connection.commit()

	def closeConnection(self):
		self.connection.close()

	def checkRecords(self):
		self.cursor.execute(f"SELECT COUNT(*) FROM {self.tableName}")
		count = self.cursor.fetchone()[0]
		if (count == 0):
			print("No Records Found!")
			return 1
		return 0

	def getFirstTableName(self):
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
		tableNames = self.cursor.fetchall()
		tableNames = [tableName[0] for tableName in tableNames]
		return tableNames[0]
		
	def getFieldsFromTable(self, tableName):
		self.cursor.execute(f"PRAGMA table_info({tableName})")
		columns = self.cursor.fetchall()
		fields = [column[1] for column in columns]
		return fields

	def getMenu(self):
		fpMenu = open(MENUFILE, "r")
		self.menu = fpMenu.read()
		fpMenu.close()

	def printMenu(self):
		print(self.menu)

	def showMenu(self):
		operations = [self.create, self.showAll, self.update, self.delete, exit]
		while True:
			self.printMenu()
			try:
				choice = int(input("Enter Your Choice: "))
				if (choice == 5):
					self.closeConnection()
				operations[choice - 1]()
			except (ValueError, IndexError):
				print("Please enter a valid number.")

Object = CRUD()

Object.showMenu()
