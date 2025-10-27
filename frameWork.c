#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MENU_FILE "menu.cfg"
#define FIELD_FILE "fields.cfg"
#define DATA_FILE "records.dat"
#define LENGTH 20


void readMenu();
void save();
void update();
void delete();
void showAll();
void printMenu();
void loadFields();
void removeNewLine(char*);
void pause();

char *menu;
char **fieldNames;
int fieldCount;
char status;

int main() {
    
    	int choice;
	readMenu();
	loadFields();
   	do {
		system("cls");
		printMenu();
		scanf("%d", &choice);
		getchar();
		switch(choice)
		{
			case 1: save(); break;
			case 2: update(); break;
			case 3: delete(); break;
			case 4: showAll(); break;
			case 5: free(menu); 
				for(int fieldCounter = 0; fieldCounter < fieldCount; fieldCounter++)
				{
					free(fieldNames[fieldCounter]);
				}
				free(fieldNames);
				exit(0);
			default: printf("Invalid Choice!\n"); pause(); break;
		}
	} while(choice != 5);

    	return 0;
}

void readMenu()
{
    	FILE *fpData = fopen(MENU_FILE, "r");
    	if (!fpData) {
        	printf("File %s Not Found.\n", MENU_FILE);
        	return;
    	}
    	
	fseek(fpData, 0, SEEK_END);
	int sizeOfFile = ftell(fpData);
	//fseek(fpData, -sizeOfFile, SEEK_CUR);
	//fseek(fpData, 0, SEEK_SET);
	rewind(fpData);
	menu = malloc(sizeOfFile + 1);
	fread(menu, sizeOfFile , 1, fpData);
	menu[sizeOfFile] = '\0';
    	fclose(fpData);
}

void save()
{
       	FILE *fpFields = fopen(FIELD_FILE, "r");
    	if (!fpFields) {
        	printf("%s not found!\n", FIELD_FILE);
        	return;
    	}

        FILE *fpData = fopen(DATA_FILE, "a");
    	if (!fpData) {
        	printf("Cannot open %s\n", DATA_FILE);
        	fclose(fpFields);
        	return;
    	}
         
    	char fieldValue[LENGTH]; 
	 
    	printf("\nAccount Details\n------------\n");

        for(int fieldCounter = 0; fieldCounter < fieldCount - 1; fieldCounter++) {
	
        	fieldNames[strcspn(fieldNames[fieldCounter], "\r\n")] = '\0';

        	printf("Enter %s: ", fieldNames[fieldCounter]);
	
        	fgets(fieldValue, sizeof(fieldValue), stdin); 
		removeNewLine(fieldValue);

		char buffer[LENGTH] = {0};

            	strncpy(buffer, fieldValue, LENGTH);

            	fwrite(buffer, LENGTH, 1, fpData);
        	
    	}
	status = 'A';
	fwrite(&status, sizeof(status), 1, fpData);

    	fclose(fpFields);
    	fclose(fpData);

    	printf("\n Record saved successfully!\n");	
	pause();
}

void update()
{
	char fieldValueToCheck[LENGTH];
	char value[LENGTH];
	char newValue[LENGTH];
	int foundValue = 0;
	printf("Enter the %s: ", fieldNames[0]);
	fgets(fieldValueToCheck, LENGTH, stdin);
	removeNewLine(fieldValueToCheck);
	FILE *fpData = fopen(DATA_FILE, "r+");
	if (!fpData)
	{
		printf("File %s Not Found\n", DATA_FILE);
		return;
	}
	while(fread(value, LENGTH, 1, fpData))
	{
		removeNewLine(value);
		if(strcmp(fieldValueToCheck, value) == 0)
		{
			printf("Match Found!\n");
			printf("Enter new %s: ", fieldNames[fieldCount - 2]);
			fgets(newValue, LENGTH, stdin);
			removeNewLine(newValue);
			fseek(fpData, ((fieldCount - 2) * LENGTH) - LENGTH , SEEK_CUR);
					
			char buffer[LENGTH] = {0};
            		strncpy(buffer, newValue, LENGTH);
			fwrite(buffer, LENGTH, 1, fpData);
			foundValue = 1;
			printf("Updated successfully!\n");
			break;
		}
		else
		{
			fseek(fpData, ((fieldCount - 2) * LENGTH + 1), SEEK_CUR);
		}
		
	}
	if(!foundValue)
	{
		printf("%s Not Found!\n", fieldValueToCheck);
	}
	fclose(fpData);
	pause();
}

void delete()
{
	char fieldValueToCheck[LENGTH];
	char value[LENGTH];
	int foundValue = 0;
	char status;
	printf("Enter the %s: ", fieldNames[0]);
	fgets(fieldValueToCheck, LENGTH, stdin);
	removeNewLine(fieldValueToCheck);
	FILE *fpData = fopen(DATA_FILE, "r+");
	if (!fpData)
	{
		printf("File %s Not Found\n", DATA_FILE);
		return;
	}
	while(fread(value, LENGTH, 1, fpData))
	{
		removeNewLine(value);
		if(strcmp(fieldValueToCheck, value) == 0)
		{
			fseek(fpData, ((fieldCount - 2) * LENGTH), SEEK_CUR);
			status = 'D';
			fwrite(&status, sizeof(status), 1, fpData);
			foundValue = 1;
			printf("Deleted %s Successfully!\n", fieldValueToCheck);
			break;
		}
		else
		{
			fseek(fpData, ((fieldCount - 2) * LENGTH + 1), SEEK_CUR);
		}
	}
	if(!foundValue)
	{
		printf("%s Not Found!\n", fieldValueToCheck);
	}
	fclose(fpData);		
	pause();
}

void showAll()
{
	int successfulRead;
	char status;
	char value[LENGTH];
        FILE *fpData = fopen(DATA_FILE, "r");
    	if (!fpData) {
        	printf("Cannot open %s\n", DATA_FILE);
        	fclose(fpData);
        	return;
    	}
	while (1) {
        	for (int fieldCounter = 0; fieldCounter < fieldCount - 1; fieldCounter++) {
			if(fieldCounter == 0) {
				fseek(fpData, (fieldCount -1) * LENGTH, SEEK_CUR);
				fread(&status, sizeof(status), 1, fpData);
			}
			if(status == 'A')
			{
				if(fieldCounter == 0)
				{
					fseek(fpData, -(((fieldCount - 1)* LENGTH) + 1), SEEK_CUR);
            			}
	
				successfulRead = fread(value, LENGTH, 1, fpData);

				if (fieldCounter == fieldCount - 2)
				{
					fseek(fpData, sizeof(status), SEEK_CUR);				 
				}
				if (successfulRead == 0)
				{
					printf("End of Records\n");
					fclose(fpData);
					pause();
					return;
				}
               			printf("%s: %s\n", fieldNames[fieldCounter], value);
			}
        	}
	}	
	fclose(fpData);
}

void printMenu()
{
	printf("%s\nEnter Your Choice: ", menu);
}

void loadFields()
{
    	FILE *fpFields = fopen(FIELD_FILE, "r");
    	if (!fpFields) {
        	printf("File %s not found!\n", FIELD_FILE);
        	return;
    	}

    	char line[LENGTH];
    	fieldCount = 0;
    	while (fgets(line, sizeof(line), fpFields)) 
	{
		fieldCount++;
	}
    	rewind(fpFields);

    	fieldNames = malloc(fieldCount * sizeof(char *));
    	for (int fieldCounter = 0; fieldCounter < fieldCount; fieldCounter++) {
        	fgets(line, sizeof(line), fpFields);
        	line[strcspn(line, "\r\n")] = '\0';
		//removeNewLine(line); 
        	fieldNames[fieldCounter] = malloc(strlen(line) + 1);
	        strcpy(fieldNames[fieldCounter], line);
    	}

    	fclose(fpFields);
}
void pause()
{
	system("pause");	
}

void removeNewLine(char *text)
{
	text[strcspn(text,"\n")] = '\0';
}