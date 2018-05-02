#!/usr/bin/env python3
#*********************************************************************
# Class:     CSCI 490
# Program:   Assignment 2
# Author:    George Zhylin
# Z-number:  z1810327
# Date Due:  3/2/18
#
# Purpose:   Practice dictionaries, list comprehensions, sorting and
#            output formatting.
#
# Execution: ./hw2.exe [filename1]
#
#
# Notes:      program loops the text file specified by the argument, 
#             reads all the lines, computes num of words and num of
#             chars. Creates a dict for chars freq, display tables 
#             that is build from the dict. Then displays word freq
#             as a table, and word freq table with some additional 
#             fields. Then program displays footers and exit
#
#**********************************************************************
from collections import defaultdict
from decimal import Decimal
import os.path
import io
import sys
import string
import operator
import math


#**************************************************************************
# Function name : buildSortTable
# Purpose       : sort & build & display table
# Arguments     : dict, columnsNumber, sortType
# Return        : none
# Author        : George Zhylin
# Date          : 3/2/18
# Notes         : Function gets 5 arguments as a dict, number of columns,  
#                 sort type,order,header. Function converts dict to a sorted 
#                 list, prints statistics for it, then builds a table and 
#                 prints it out.
#
#***************************************************************************
def buildSortTable (charDict, numCol, sortType, order, header):
	#declare variables  
	listSorted = []                                 #list to hold sorted dict
	tempString = ""                                 #temp string
	sortBy = "By key"                               #type of sort 
	rcList = []                                     #row to col ratio
	output = ""                                     #to hold output
  
	#adjust sort type display
	if sortType == 0:
		sortBy = "By value"

	#make a sorted list
	if sortType == 1:               #sort by the key
		for q,w in sorted(charDict.items()):
			#1 space for 1st arg q and 5space for 2'nd arg w
			tempString = "{0:2} = {1:5}".format (q,w) 
			listSorted.append(tempString)
	else:                           #sort by the value
		if (order == 1):              #print in desc order
			for q in sorted(charDict, key=charDict.get):
				tempString = "{0:2} = {1:5}".format (q,charDict[q])
				listSorted.append(tempString)
		else:
			for q in sorted(charDict, key=charDict.get, reverse= True):
				tempString = "{0:2} = {1:5}".format (q,charDict[q])
				listSorted.append(tempString)
	
	#get number of rows and number of entrys in a sorted list
	numRows = math.ceil(len(listSorted)/numCol)
	totalR = len(listSorted)                   
  
	#make a list of row to columns ratio
	#ex. rcList[0]=6 first column has 6 rows
	for i in range(numCol):
		if numRows < totalR:
			rcList.append(numRows)
			totalR = totalR - numRows
		else:
			rcList.append(totalR)
      
	print("")
	print("Building a table...")
	print("Number of entry's in dict :      ",len(listSorted))
	print("Type of dict sort :              ",sortBy)
	print("Number of columns in the table : ",numCol)
	print("Number of rows in a table :      ",numRows)
	print("Number of rows in a columns :    ",rcList)
	print(" ")
	print(header)
  
	#bulding a table
	for i in range(numRows):                            #range as numRows
		for x in range(len(rcList)):                    #range as numEntrys
			if rcList[x] > 0:                           #if ratio > 0
				output += listSorted[i+(numRows*x)]     #append to string
				output += "   "                         #append space
				rcList[x] = rcList[x]-1                 #update counter
		print(output)                                   #print line
		output = ""                                     #clear string
	
	return


#check if 1 arguments provided
if len (sys.argv) < 2 :
	print ("Error, argument is not provided.")
	exit()

print(" ")
print("no. of arguments = ", len(sys.argv))
print("arguments are: ", sys.argv)

#declare variables 
letterDict = defaultdict(int) 
wordDict = defaultdict(int)
totalRecords = 0
totalChars = 0
totalCharsCounted = 0
countChars = 0
countWords = 0
countDistChars = 0
 
#open file to read
textFile = open(sys.argv[1], encoding="ISO-8859-15")

  
#start processing file one line at a time
while True:
	output = textFile.readline()
	totalRecords += 1
		
	#convert to lower-case & replace double hypen
	output = output.lower()
	output = output.replace("--","  ")
	
	#check each char in output string
	for char in output:
		
		totalChars += 1
		
		#if not an letter or ' and - then replace with space
		if char not in string.ascii_lowercase :
			if char not in ["'","-"]:
				output = output.replace(char, " ")
	
	#populate dict
	for char in output:
		if char not in ["'","-"," "]:
			letterDict[char] += 1
			totalCharsCounted += 1
			
	#split words in a string and count len
	splitOutput = output.split()
	for word in splitOutput:
		wordDict[len(word)] += 1
		countWords += 1
		
	#if empty line, end loop
	if output == '':
		break


# close the text file
textFile.close()

#build a freq table 
buildSortTable(letterDict,5,1,1,"") #arg 1=dict,2=NofColumns,3=sortType,4=order,5=header
buildSortTable(letterDict,5,0,0,"") #arg 1=dict,2=NofColumns,3=sortType,4=order,5=header

#build word len freq table
print(" ")
buildSortTable(wordDict,5,1,1,"len  count   len  count   len  count   len  count   len  count   ")
 
#build word len freq desc table
print("")
print("rank length   freq  len*fre rank*fre lgf/lgr ")

#declare some data
tempStr = ""
listWord = []
listOutStr = ""
listFreqOnly = []    #sorted list with only freq data
rank = 1

#build a list
for q in sorted(wordDict, key=wordDict.get, reverse= True):
	tempStr = "{0:2}  {1:5}    {2:5}".format (q,wordDict[q],(q * wordDict[q]))
	listWord.append(tempStr)
	tempStr = ""
	tempStr = "{0:5}".format (wordDict[q])
	listFreqOnly.append(tempStr)
	tempStr = ""

#build a table
for l in range(len(listWord)):
	if rank == 1:
		listOutStr += "  {0:2}     {1:18}    ".format (rank,listWord[l])
		listOutStr += "{0:5}".format (rank * listFreqOnly[l])
		rank += 1
		print(listOutStr)
		listOutStr = ""
	else:
		listOutStr += "  {0:2}     {1:18}    ".format (rank,listWord[l])
		listOutStr += "{0:5}    ".format (rank * int(listFreqOnly[l]))
		listOutStr += "{0:.2f}".format (math.log(int(listFreqOnly[l]),2)/math.log(rank,2))
		rank += 1
		print(listOutStr)
		listOutStr = ""
	

#print output footers
print(" ")
print("Records read:        {0:6}".format(totalRecords))
print("Characters read:     {0:6}".format(totalChars))
print("Characters counted:  {0:6}".format(totalCharsCounted))
print("Words read :         {0:6}".format(countWords))
print("Distinct characters :{0:6}".format(len(letterDict )))
print(" ")



