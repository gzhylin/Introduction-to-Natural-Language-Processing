#!/usr/bin/env python3
#*********************************************************************
# Class:     CSCI 490
# Program:   Assignment 3
# Author:    George Zhylin
# Z-number:  z1810327
# Date Due:  5/1/18
#
# Purpose:   Implement Kernighan’s spelling algorithm using a real-world dataset.
#
# Execution: ./hw3.py
#
#
# Notes:      
#
#**********************************************************************
import string
import time
import pickle
import os.path
import sys
import string

# Class Item
# Purpose to hold prepared data
class Item:
	def __init__(self):
		self.dictUni = {}
		self.dictBi = {}
		self.dictW = {}
		self.dictBT = {}
		self.totalW = 0
		
# Class Word
# Purpose to hold word object
class Word:
	def __init__(self,word,cType,cLetters,corpusN, probN, magicN):
		self.word = word
		self.cType = cType
		self.cLetters = cLetters
		self.corpusN = corpusN
		self.probN = probN
		self.magicN = magicN
		
# Fuction doDicts
# input list of lists as a 
# confusion matrices from Kernighan’s paper
# convert to the dict of dicts
def doDicts(list):
	dict = {}
	for i in list:
		dict[i[0]]={}
		for b in range(len(string.ascii_lowercase)):
			dict[i[0]][string.ascii_lowercase[b]] = i[b+1]
	return dict

# Declare variables
fileName = "pickle.dat"
fileExists = False
statusLine = "Need to run!"

# Check if argument exists
if len(sys.argv) == 2:
	# If we have correct number of arguments which is 2
	# save the testSring and continue to the next step
	testSring = sys.argv[1]
	# Check if pickle file with data dicts exist
	if os.path.exists(fileName):
		fileExists = True
		statusLine = "Completed!  "
  
	# Display simple menu
	print("****************************************************")
	print("*    Spell checking using Kernighan’s algorithm    *")
	print("*                                                  *")
	print("*    Prepared data status:  ",statusLine,"         *")
	print("*                                                  *")
	print("****************************************************")
  
	# If file does not exist, promt to prepare and save
	if fileExists == False:
		answer = input('Prepare the data and save? Y or N ... ')
		if answer == 'Y' or answer == 'y' or answer == "yes":
			# PREPARE THE DATA
			print("Please wait...")
			# Open file to read from

			stream = open("/home/turing/t90rkf1/dnl/dhw/data/ap88.txt","r")

			# create Item Obj to save all the data
			one = Item()
			lineNum = 1
			# start time ounters
			startElapsedT = time.perf_counter()
			startCPUtime = time.process_time()

			# read
			while True:
				print("Reading line ",lineNum)
				lineNum += 1
				line = stream.readline()
				firstWord = False
				# Step 1: Remove all chars that are not ascii_letters
				# Step 2: Convert to lower case
				# Step 3: Split the string in tokens and put in listTok
				# Step 4: Add "<" and ">" at both ends on every string
				# Step 5: Process unigrams and save to dict. Start by 
				#         looking at every word in listTok, skip first 
				#         word id (ex. AP880212-0001 ) then check dictW
				#         if this word is present, if not insert. Before
                #         inserting remove < and >  then
				#         update the total words counter. Finally check
				#         every char in a string and update unigram dict
				# Step 6: Process bigrams and save to dict. Following
				#         previous step, after collecting all the unigrams
				#         we start processing bigrams with a sliding window
				#         technique. 
        
				#1
				for b in line:
					if b not in string.ascii_letters:
						line = line.replace(b, " ")
					
				#2
				line = line.lower()
				  
				#3
				listTok = line.split()
				
				#4
				for c in range(len(listTok)):
					listTok[c] = "<" + listTok[c] + ">"
				
				#5
				for word in listTok:
					if firstWord == False:
						firstWord = True
					else:
						word2 = word.replace("<", "")
						word3 = word2.replace(">", "")
						if one.dictW.get(word3):
							count = (one.dictW.get(word3))
							one.dictW[word3] = count +1
						else:
							one.dictW[word3] = 1
						one.totalW += 1
						for c in word:
							if one.dictUni.get(c):
								count = (one.dictUni.get(c))
								one.dictUni[c] = count +1
							else:
								one.dictUni[c] = 1
				#6    
						for letter in range(0,len(word)-1):
							if one.dictBi.get(word[letter]+(word[letter+1])):
								count = (one.dictBi.get(word[letter]+(word[letter+1])))
								one.dictBi[word[letter]+(word[letter+1])] = count +1 
							else:
								one.dictBi[word[letter]+(word[letter+1])] = 1
				
				# reach eof, close stream
				if not line:
					break
        
			# end time 
			endElapsedT = time.perf_counter()
			endCPUtime = time.process_time()

			print ("----------------------------------------------------")
			print ("Start elapsed time :      ", startElapsedT)
			print ("Start CPU time :          ", startCPUtime)
			print ("End elapsed time :        ", endElapsedT)
			print ("End CPU time :            ", endCPUtime)
			print ("----------------------------------------------------")
			print ("Total elapsed time :      ", (endElapsedT - startElapsedT))
			print ("Total CPU time :          ", (endCPUtime - startCPUtime))
			print ("----------------------------------------------------")
			print ("Number of words:          ", one.totalW)
			print ("Number of distinct words: ", len(one.dictW))
			print ("Number of Bigrams:        ", len(one.dictBi))
			print ("Number of Unigrams:       ", len(one.dictUni))
			print ("----------------------------------------------------")
			print ("Unigram counts:")

			for i in (sorted(one.dictUni)):
				print(i,one.dictUni[i])
      
			print("Bigram row totals:")
      
			for i in (sorted(one.dictBi)):
				flagBT = False
				for c in i:
					if flagBT == False:
						flagBT = True
						if one.dictBT.get(c):
							count = (one.dictBT.get(c))
							one.dictBT[c] = (one.dictBi.get(i)) + count
						else:
							one.dictBT[c] = (one.dictBi.get(i))
			for i in (sorted(one.dictBT)):
				print(i,"row, total = ",one.dictBT[i])
      
			print("Bigram counts:")
      
			for i in (sorted(one.dictBi)):
				print(i,one.dictBi[i])
        
			# open the file for writing
			fileObject = open(fileName,'wb') 

			# this writes the object one a to the file 
			pickle.dump(one,fileObject)   

			# here we close the fileObject
			fileObject.close()
			
			print(" ")
			print("Data file 'pickle' saved to a local folder...")
			print("Please restart the program to continue...")
			sys.exit()
			
    
    # In case user dont want to prepare the data
	else:
		print("Word to be checked: ", testSring)
		print("Creating a list of possible corrections...")

		# Creating possible corrections

		# ***TRS***
		# Transpose any two consecutive letters
		# swap letters, and save new string in
		# listTrs dict as well as swaped letters
		listTrs = {}
	  
		for pos in range(len(testSring)-1):
			listTrs[testSring[:pos] + testSring[pos+1] + testSring[pos] + testSring[pos+2:]]= testSring[pos+1] +'|'+ testSring[pos]
	  
		# *** SUB ***
		# Substitute the letter at any position with any other
		# letter. Save new string and letter to the listSub dict
		listSub = {}

		for pos in range(len(testSring)):
			for char in string.ascii_lowercase:
				listSub[(testSring[:pos] + char + testSring[pos+1:])] = (testSring[pos]+'|'+char)

	  
		# *** DEL ***
		# Delete a letter at any position in a string
		# save new string and deleted letter in a listDelete dict
		listDelete = {}

		for pos in range(len(testSring)):
			listDelete[(testSring[:pos] + testSring[pos+1:])] = (testSring[pos-1]+'|'+testSring[pos])

	  
		# *** ADD ***
		# Add space in the end, to make life easy.
		# loop thru every position string, inserting
		# characters a to z, saving new string in a 
		# listAdd.
		listAdd = {}

		for pos in range(len(testSring)):
			for char in string.ascii_lowercase:
				listAdd[(testSring[:pos] + char + testSring[pos:])] = testSring[pos-1]+'|'+char
	  
	  
		print("Possible corrections created! Here is the info...")
		print("Items in a Add list = {}".format(len(listAdd)))
		print("Items in a Del list = {}".format(len(listDelete)))
		print("Items in a Sub list = {}".format(len(listSub)))
		print("Items in a Trs list = {}".format(len(listTrs)))
		print("Total number of possible corrections: ",(len(listAdd))+(len(listDelete))+(len(listSub))+(len(listTrs)))
		print("Checking the Corpus to see if the these words are real...")

		# the confusion matrices from Kernighan’s paper
		# ---------------------------------------------
		# del[X, Y] = Deletion of Y after X
		# outer subscript = X
		# inner subscript = Y (deleted letter)

		del_table =[['a',0,7,58,21,3,5,18,8,61,0,4,43,5,53,0,9,0,98,28,53,62,1,0,0,2,0],
				   	['b',2,2,1,0,22,0,0,0,183,0,0,26,0,0,2,0,0,6,17,0,6,1,0,0,0,0],
					['c',37,0,70,0,63,0,0,24,320,0,9,17,0,0,33,0,0,46,6,54,17,0,0,0,1,0],
					['d',12,0,7,25,45,0,10,0,62,1,1,8,4,3,3,0,0,11,1,0,3,2,0,0,6,0],
					['e',80,1,50,74,89,3,1,1,6,0,0,32,9,76,19,9,1,237,223,34,8,2,1,7,1,0],
					['f',4,0,0,0,13,46,0,0,79,0,0,12,0,0,4,0,0,11,0,8,1,0,0,0,1,0],
					['g',25,0,0,2,83,1,37,25,39,0,0,3,0,29,4,0,0,52,7,1,22,0,0,0,1,0],
					['h',15,12,1,3,20,0,0,25,24,0,0,7,1,9,22,0,0,15,1,26,0,0,1,0,1,0],
					['i',26,1,60,26,23,1,9,0,1,0,0,38,14,82,41,7,0,16,71,64,1,1,0,0,1,7],
					['j',0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0],
					['k',4,0,0,1,15,1,8,1,5,0,1,3,0,17,0,0,0,1,5,0,0,0,1,0,0,0],
					['l',24,0,1,6,48,0,0,0,217,0,0,211,2,0,29,0,0,2,12,7,3,2,0,0,11,0],
					['m',15,10,0,0,33,0,0,1,42,0,0,0,180,7,7,31,0,0,9,0,4,0,0,0,0,0],
					['n',21,0,42,71,68,1,160,0,191,0,0,0,17,144,21,0,0,0,127,87,43,1,1,0,2,0],
					['o',11,4,3,6,8,0,5,0,4,1,0,13,9,70,26,20,0,98,20,13,47,2,5,0,1,0],
					['p',25,0,0,0,22,0,0,12,15,0,0,28,1,0,30,93,0,58,1,18,2,0,0,0,0,0],
					['q',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,18,0,0,0,0,0],
					['r',63,4,12,19,188,0,11,5,132,0,3,33,7,157,21,2,0,277,103,68,0,10,1,0,27,0],
					['s',16,0,27,0,74,1,0,18,231,0,0,2,1,0,30,30,0,4,265,124,21,0,0,0,1,0],
					['t',24,1,2,0,76,1,7,49,427,0,0,31,3,3,11,1,0,203,5,137,14,0,4,0,2,0],
					['u',26,6,9,10,15,0,1,0,28,0,0,39,2,111,1,0,0,129,31,66,0,0,0,0,1,0],
					['v',9,0,0,0,58,0,0,0,31,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,1,0],
					['w',40,0,0,1,11,1,0,11,15,0,0,1,0,2,2,0,0,2,24,0,0,0,0,0,0,0],
					['x',1,0,17,0,3,0,0,1,0,0,0,0,0,0,0,6,0,0,0,5,0,0,0,0,1,0],
					['y',2,1,34,0,2,0,1,0,1,0,0,1,2,1,1,1,0,0,17,1,0,0,1,0,0,0],
					['z',1,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
					['@',20,14,41,31,20,20,7,6,20,3,6,22,16,5,5,17,0,28,26,6,2,1,24,0,0,2]]

		# add[X Y] = Insertion of Y after X
		# outer subscript = X
		# inner subscript = Y (Inserted Letter)

		add_table =[['a',15,1,14,7,10,0,1,1,33,1,4,31,2,39,12,4,3,28,134,7,28,0,1,1,4,1],
					['b',3,11,0,0,7,0,1,0,50,0,0,15,0,1,1,0,0,5,16,0,0,3,0,0,0,0],
					['c',19,0,54,1,13,0,0,18,50,0,3,1,1,1,7,1,0,7,25,7,8,4,0,1,0,0],
					['d',18,0,3,17,14,2,0,0,9,0,0,6,1,9,13,0,0,6,119,0,0,0,0,0,5,0],
					['e',39,2,8,76,147,2,0,1,4,0,3,4,6,27,5,1,0,83,417,6,4,1,10,2,8,0],
					['f',1,0,0,0,2,27,1,0,12,0,0,10,0,0,0,0,0,5,23,0,1,0,0,0,1,0],
					['g',8,0,0,0,5,1,5,12,8,0,0,2,0,1,1,0,1,5,69,2,3,0,1,0,0,0],
					['h',4,1,0,1,24,0,10,18,17,2,0,1,0,1,4,0,0,16,24,22,1,0,5,0,3,0],
					['i',10,3,13,13,25,0,1,1,69,2,1,17,11,33,27,1,0,9,30,29,11,0,0,1,0,1],
					['j',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
					['k',2,4,0,1,9,0,0,1,1,0,1,1,0,0,2,1,0,0,95,0,1,0,0,0,4,0],
					['l',3,1,0,1,38,0,0,0,79,0,2,128,1,0,7,0,0,0,97,7,3,1,0,0,2,0],
					['m',11,1,1,0,17,0,0,1,6,0,1,0,102,44,7,2,0,0,47,1,2,0,1,0,0,0],
					['n',15,5,7,13,52,4,17,0,34,0,1,1,26,99,12,0,0,2,156,53,1,1,0,0,1,0],
					['o',14,1,1,3,7,2,1,0,28,1,0,6,3,13,64,30,0,16,59,4,19,1,0,0,1,1],
					['p',23,0,1,1,10,0,0,20,3,0,0,2,0,0,26,70,0,29,52,9,1,1,1,0,0,0],
					['q',0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
					['r',15,2,1,0,89,1,1,2,64,0,0,5,9,7,10,0,0,132,273,29,7,0,1,0,10,0],
					['s',13,1,7,20,41,0,1,50,101,0,2,2,10,7,3,1,0,1,205,49,7,0,1,0,7,0],
					['t',39,0,0,3,65,1,10,24,59,1,0,6,3,1,23,1,0,54,264,183,11,0,5,0,6,0],
					['u',15,0,3,0,9,0,0,1,24,1,1,3,3,9,1,3,0,49,19,27,26,0,0,2,3,0],
					['v',0,2,0,0,36,0,0,0,10,0,0,1,0,1,0,1,0,0,0,0,1,5,1,0,0,0],
					['w',0,0,0,1,10,0,0,1,1,0,1,1,0,2,0,0,1,1,8,0,2,0,4,0,0,0],
					['x',0,0,18,0,1,0,0,6,1,0,0,0,1,0,3,0,0,0,2,0,0,0,0,1,0,0],
					['y',5,1,2,0,3,0,0,0,2,0,0,1,1,6,0,0,0,1,33,1,13,0,1,0,2,0],
					['z',2,0,0,0,5,1,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4],
					['@',46,8,9,8,26,11,14,3,5,1,17,5,6,2,2,10,0,6,23,2,11,1,2,1,1,2]]

		# sub[X Y] = Substitution of X (incorrect) for Y (correct)
		# outer subscript = X
		# inner subscript = Y (correct)

		sub_table =[['a',0,0,7,1,342,0,0,2,118,0,1,0,0,3,76,0,0,1,35,9,9,0,1,0,5,0],
					['b',0,0,9,9,2,2,3,1,0,0,0,5,11,5,0,10,0,0,2,1,0,0,8,0,0,0],
					['c',6,5,0,16,0,9,5,0,0,0,1,0,7,9,1,10,2,5,39,40,1,3,7,1,1,0],
					['d',1,10,13,0,12,0,5,5,0,0,2,3,7,3,0,1,0,43,30,22,0,0,4,0,2,0],
					['e',388,0,3,11,0,2,2,0,89,0,0,3,0,5,93,0,0,14,12,6,15,0,1,0,18,0],
					['f',0,15,0,3,1,0,5,2,0,0,0,3,4,1,0,0,0,6,4,12,0,0,2,0,0,0],
					['g',4,1,11,11,9,2,0,0,0,1,1,3,0,0,2,1,3,5,13,21,0,0,1,0,3,0],
					['h',1,8,0,3,0,0,0,0,0,0,2,0,12,14,2,3,0,3,1,11,0,0,2,0,0,0],
					['i',103,0,0,0,146,0,1,0,0,0,0,6,0,0,49,0,0,0,2,1,47,0,2,1,15,0],
					['j',0,1,1,9,0,0,1,0,0,0,0,2,1,0,0,0,0,0,5,0,0,0,0,0,0,0],
					['k',1,2,8,4,1,1,2,5,0,0,0,0,5,0,2,0,0,0,6,0,0,0,.4,0,0,3],
					['l',2,10,1,4,0,4,5,6,13,0,1,0,0,14,2,5,0,11,10,2,0,0,0,0,0,0],
					['m',1,3,7,8,0,2,0,6,0,0,4,4,0,180,0,6,0,0,9,15,13,3,2,2,3,0],
					['n',2,7,6,5,3,0,1,19,1,0,4,35,78,0,0,7,0,28,5,7,0,0,1,2,0,2],
					['o',91,1,1,3,116,0,0,0,25,0,2,0,0,0,0,14,0,2,4,14,39,0,0,0,18,0],
					['p',0,11,1,2,0,6,5,0,2,9,0,2,7,6,15,0,0,1,3,6,0,4,1,0,0,0],
					['q',0,0,1,0,0,0,27,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					['r',0,14,0,30,12,2,2,8,2,0,5,8,4,20,1,14,0,0,12,22,4,0,0,1,0,0],
					['s',11,8,27,33,35,4,0,1,0,1,0,27,0,6,1,7,0,14,0,15,0,0,5,3,20,1],
					['t',3,4,9,42,7,5,19,5,0,1,0,14,9,5,5,6,0,11,37,0,0,2,19,0,7,6],
					['u',20,0,0,0,44,0,0,0,64,0,0,0,0,2,43,0,0,4,0,0,0,0,2,0,8,0],
					['v',0,0,7,0,0,3,0,0,0,0,0,1,0,0,1,0,0,0,8,3,0,0,0,0,0,0],
					['w',2,2,1,0,1,0,0,2,0,0,1,0,0,0,0,7,0,6,3,3,1,0,0,0,0,0],
					['x',0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,0,0],
					['y',0,0,2,0,15,0,1,7,15,0,0,0,2,0,6,1,0,7,36,8,5,0,0,1,0,0],
					['z',0,0,0,7,0,0,0,0,0,0,0,7,5,0,0,0,0,2,21,3,0,0,0,0,3,0]]

		# transpose[X  Y] = Reversal of XY
		# outer subscript = X
		# inner subscript = Y

		transpose_table = [['a',0,0,2,1,1,0,0,0,19,0,1,14,4,25,10,3,0,27,3,5,31,0,0,0,0,0],
						['b',0,0,0,0,2,0,0,0,0,0,0,1,1,0,2,0,0,0,2,0,0,0,0,0,0,0],
						['c',0,0,0,0,1,0,0,1,85,0,0,15,0,0,13,0,0,0,3,0,7,0,0,0,0,0],
						['d',0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0],
						['e',1,0,4,5,0,0,0,0,60,0,0,21,6,16,11,2,0,29,5,0,85,0,0,0,2,0],
						['f',0,0,0,0,0,0,0,0,12,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						['g',4,0,0,0,2,0,0,0,0,0,0,1,0,15,0,0,0,3,0,0,3,0,0,0,0,0],
						['h',12,0,0,0,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0],
						['i',15,8,31,3,66,1,3,0,0,0,0,9,0,5,11,0,1,13,42,35,0,6,0,0,0,3],
						['j',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						['k',0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						['l',11,0,0,12,20,0,1,0,4,0,0,0,0,0,1,3,0,0,1,1,3,9,0,0,7,0],
						['m',9,0,0,0,20,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,4,0,0,0,0,0],
						['n',15,0,6,2,12,0,8,0,1,0,0,0,3,0,0,0,0,0,6,4,0,0,0,0,0,0],
						['o',5,0,2,0,4,0,0,0,5,0,0,1,0,5,0,1,0,11,1,1,0,0,7,1,0,0],
						['p',17,0,0,0,4,0,0,1,0,0,0,0,0,0,1,0,0,5,3,6,0,0,0,0,0,0],
						['q',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						['r',12,0,0,0,24,0,3,0,14,0,2,2,0,7,30,1,0,0,0,2,10,0,0,0,2,0],
						['s',4,0,0,0,9,0,0,5,15,0,0,5,2,0,1,22,0,0,0,1,3,0,0,0,16,0],
						['t',4,0,3,0,4,0,0,21,49,0,0,4,0,0,3,0,0,5,0,0,11,0,2,0,0,0],
						['u',22,0,5,1,1,0,2,0,2,0,0,2,1,0,20,2,0,11,11,2,0,0,0,0,0,0],
						['v',0,0,0,0,1,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						['w',0,0,0,0,0,0,0,4,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,8,0],
						['x',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
						['y',0,1,2,0,0,0,1,0,0,0,0,3,0,0,0,2,0,1,10,0,0,0,0,0,0,0],
						['z',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

		# convert tables to dict of dicts
		dictConfTrs = doDicts(transpose_table)
		dictConfAdd = doDicts(add_table)
		dictConfDel = doDicts(del_table)
		dictConfSub = doDicts(sub_table)
		
		# Load data from the file
		# we open the file for reading in BINARY
		fileObject = open(fileName,'rb')  
		two = pickle.load(fileObject)  
		fileObject.close
		
		# List of words after checking them in a corpusN
		# Only real words left. check each dict for words 
		# in corpus, if found, display word, stats, and 
		# convert all that info into the new object Word
		# and append it to the list finallist
		# 
		# object Word :
		# word,cType,cLetters,corpusN, probN, magicN  
		
		# list to hold all the Word objects
		finalList = []

		for word, stat in two.dictW.items():
			# ADD dict
			for wordAdd in listAdd:
				if wordAdd == word:
					print(word, two.dictW.get(word))
					# Smoothing = we will add .5 to each count so no count
					# will be zero even though
					# many words aren’t found in any given corpus. 
					pValue = ((two.dictW.get(word)+0.5)/((two.totalW)+(len(two.dictW)*0.5)))
					
					xy = listAdd.get(word)
					x = xy[0] # letter before inserted letter
					y = xy[2] # inserted letter
					xyValue = dictConfAdd[x][y]
					pXW = (xyValue/(two.dictUni.get(x)))
					
					# magic formula					
					pM = (1000000000*pValue*pXW)
					
					# Create new object type Word and add to the list
					item = Word(word,"Add Y=XY",listAdd.get(word),pValue,pXW,pM)
					finalList.append(item);
					
			# DELETE dict
			for wordDel in listDelete:
				if wordDel == word:
					print(word, two.dictW.get(word))
					# Smoothing = we will add .5 to each count so no count
					# will be zero even though
					# many words aren’t found in any given corpus. 
					pValue = ((two.dictW.get(word)+0.5)/((two.totalW)+(len(two.dictW)*0.5)))
					
					xAy = listDelete.get(word)
					xy = xAy[0]+xAy[2] # ex. convert from a|b to ab
					x = xy[0] #letter before the letter to be del
					y = xy[1] #letter to be deleted
					xyValue = dictConfDel[x][y]
					pXW = (xyValue/((two.dictBi.get(xy))))
					
					# magic formula					
					pM = (1000000000*pValue*pXW)
					
					# Create new object type Word and add to the list
					item = Word(word,"Del Y=XY",listDelete.get(word),pValue,pXW,pM)
					finalList.append(item);

			# SUB dict
			for wordSub in listSub:
				if wordSub == word:
					print(word, two.dictW.get(word))
					# Smoothing = we will add .5 to each count so no count
					# will be zero even though
					# many words aren’t found in any given corpus. 
					pValue = ((two.dictW.get(word)+0.5)/((two.totalW)+(len(two.dictW)*0.5)))
										
					xy = listSub.get(word)
					x = xy[0] # original letter
					y = xy[2] # inserted letter
					xyValue = dictConfSub[x][y]
					pXW = (xyValue/(two.dictUni.get(y)))
					
					# magic formula					
					pM = (1000000000*pValue*pXW)
					
					# Create new object type Word and add to the list
					item = Word(word,"Sub X=Y ",listSub.get(word),pValue,pXW,pM)
					finalList.append(item);

			# TRS dict
			for wordTrs in listTrs:
				if wordTrs == word:
					print(word, two.dictW.get(word))
					# Smoothing = we will add .5 to each count so no count
					# will be zero even though
					# many words aren’t found in any given corpus. 
					pValue = ((two.dictW.get(word)+0.5)/((two.totalW)+(len(two.dictW)*0.5)))
															
					xAy = listTrs.get(word)
					xy = xAy[0]+xAy[2] # ex. convert from a|b to ab
					x = xy[0] # swap 
					y = xy[1] # swap
					xyValue = dictConfTrs[x][y]
					pXW = (xyValue/(two.dictBi.get(xy)))
					
					# magic formula					
					pM = (1000000000*pValue*pXW)
					
					# Create new object type Word and add to the list
					item = Word(word,"Trs X=Y ",listTrs.get(word),pValue,pXW,pM)
					finalList.append(item);
		
		# sort the list of objects
		finalList.sort(key=lambda x: x.magicN, reverse=True)
					
		print("")
		print("After looking up the corpus, only ", len(finalList), " words left.")
		print("")
		print("-----------------------------------------------------------------------------")
		print("   Word entered to be checked :  ",sys.argv[1])
		print("-----------------------------------------------------------------------------")
		print("   Candidate   |  Error  |  Error  | P(x|word)  |  P(word)  | 10^9*P(x|w)P(w)")
		print("  Correction   |  Type   | Letters | Confusion  | Frequency |     Magic      ")
		print("     Word      |         |  X | Y  | Matrices   | In CORPUS |    Formula     ")
		print("-----------------------------------------------------------------------------")
		
		# Display formated output
		for i in range(len(finalList)):
			print(
			"{:>12s}".format(finalList[i].word)," ",
			"{:>9s}".format(finalList[i].cType)," ",
			"{:>5s}".format(finalList[i].cLetters),"  ",
			"{:.9f}".format(finalList[i].probN)," ",
			"{:.9f}".format(finalList[i].corpusN)," ",
			"{:.9f}".format(finalList[i].magicN))
		print("")

# in case incorrect number of arguments entered, exit
else: 
	print("Incorect arguments or no arguments entered... exit...")
	sys.exit()
  