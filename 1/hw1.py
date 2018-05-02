#
#Class:     CSCI 490
#Program:   Assignment 1
#Author:    George Zhylin
#Z-number:  z1810327
#Date Due:  2/20/18
#
#Purpose:   Read and Process text file.
#
#Execution: ./hw1.exe [filename1] [filename2]
#
#
#Notes:     Program opens a file one by one, processes it, dispays usefull data
#           and stores is in object, and later this 2 objects used to calculate
#           chi-square.
#
#
#

import os.path
import io
import sys

#
# Class name : textInfo
# Purpose : to save data after processing a text file
#

class textInfo:
  vowels = 0
  consonants = 0
  name = "none"

#
# Function Name:  check
# Arguments : (string) path
# Notes:     Function gets path as an argument, checks if it valid.
#            Creates temp object to save data. Starts reading a file
#            one line at a time, calculates number of special chars
#            and keeps track of other counters. When done reading a
#            file, it displays calculated info, then saves data to the
#            object and returns it.
#
# Return:  textInfo object
#
def check (path):

  #check if file exist, if not exit
  if os.path.exists(path) == False:
        print("Requested file ", path, " does not exist, program will exit.")
        exit()

  #create instance of a object to save the data
  thisTextInfo = textInfo()
  thisTextInfo.name = path
  #open file to read
  textFile = open(path, encoding="utf-8")
  #declare counters
  lineCounter = 0
  charCounter = 0
  letterCounter = 0
  #declare counters for each specific letter
  #note: probably not the best idea to name them this way
  a = 0
  b = 0
  c = 0
  d = 0
  e = 0
  f = 0
  g = 0
  h = 0
  i = 0
  j = 0
  k = 0
  l = 0
  ea = 0
  ee = 0
  ei = 0
  eo = 0
  eu = 0
  total = 0

  #start processing file one line at a time
  while True:
    output = textFile.readline()

    #convert to lower-case
    output.lower()
    #check each char in output string
    for char in output:
      if char == "a":
        ea+=1
      if char == "e":
        ee+=1
      if char == "i":
        ei+=1
      if char == "o":
        eo+=1
      if char == "u":
        eu+=1
      if char == "\u00e9":
        a+=1
      if char == "\u00e2":
        b+=1
      if char == "\u00ea":
        c+=1
      if char == "\u00ee":
        d+=1
      if char == "\u00f4":
        e+=1
      if char == "\u00fb":
        f+=1
      if char == "\u00e0":
        g+=1
      if char == "\u00e8":
        h+=1
      if char == "\u00f9":
        i+=1
      if char == "\u00eb":
        j+=1
      if char == "\u00ef":
        k+=1
      if char == "\u00fc":
        l+=1
      letterCounter += 1

    charCounter = charCounter + len(output)
    lineCounter+=1
    #if empty line, end loop
    if output == '':
      break
  # close the text file
  textFile.close()
  #calculate totals
  total = a+b+c+d+e+f+g+h+i+j+k+l+ea+ee+ei+eo+eu

  #print output for the file
  print(" ")
  print("Information on a file ", path)
  print("Total is ", lineCounter -1 , " lines in this text.")
  print("Total is ",charCounter, " char's in this text.")
  print("Character -","\u00e9", "- appears : ",a, " times.")
  print("Character -","\u00e2", "- appears : ",b, " times.")
  print("Character -","\u00ea", "- appears : ",c, " times.")
  print("Character -","\u00ee", "- appears : ",d, " times.")
  print("Character -","\u00f4", "- appears : ",e, " times.")
  print("Character -","\u00fb", "- appears : ",f, " times.")
  print("Character -","\u00e0", "- appears : ",g, " times.")
  print("Character -","\u00e8", "- appears : ",h, " times.")
  print("Character -","\u00f9", "- appears : ",i, " times.")
  print("Character -","\u00eb", "- appears : ",j, " times.")
  print("Character -","\u00ef", "- appears : ",k, " times.")
  print("Character -","\u00fc", "- appears : ",l, " times.")
  print("Character -","a", "- appears : ",ea, " times.")
  print("Character -","e", "- appears : ",ee, " times.")
  print("Character -","i", "- appears : ",ei, " times.")
  print("Character -","o", "- appears : ",eo, " times.")
  print("Character -","u", "- appears : ",eu, " times.")
  print("Total number of vowels is ", total)
  print("Total number of consonants is ", charCounter - total)
  print("Total is ",letterCounter, " letters in this text.")
  print("Percentage of vowels is ", round((total / charCounter),2))
  print("System utility used to check output is wc -m.")
  print(" ")

  #save data to the objects and return it
  thisTextInfo.vowels = total
  thisTextInfo.consonants = letterCounter - total
  return thisTextInfo


#check if 2 arguments provided
if len (sys.argv) < 3 :
        print ("Error, two arguments are not provided.")
        exit()

#set file names
pathOne = sys.argv[1]
pathTwo = sys.argv[2]

#create object for first file
textOne = textInfo()
textOne = check(pathOne)

#create object for second file
textTwo = textInfo()
textTwo = check(pathTwo)

#Calculation for the chi-square
textOneVandC = textOne.vowels + textOne.consonants
textTwoVandC = textTwo.vowels + textTwo.consonants

Vowel1and2 = textOne.vowels     + textTwo.vowels
Cons1and2  = textOne.consonants + textTwo.consonants

total = textOneVandC + textTwoVandC

#sample visualisation of my contingency table
#
# textOne.vovels = tOneV  |    textOne.consonants = tOneC  |  <- textOneVandC
# -------------------------------------------------------
# textTwo.vowels = tTwoV  |    textTwo.consonants = tTwoC  |  <- textTwoVandC
# ---------------------------------------------------------------------------
#        Vovel1and2       |         Cons1and2              |       total
#

tOneV = (Vowel1and2/total)*textOneVandC
tOneC = ( Cons1and2/total)*textOneVandC
tTwoV = (Vowel1and2/total)*textTwoVandC
tTwoC = ( Cons1and2/total)*textTwoVandC

tOneV = ((textOne.vowels     - tOneV)**2)/tOneV
tOneC = ((textOne.consonants - tOneC)**2)/tOneC
tTwoV = ((textTwo.vowels     - tTwoV)**2)/tTwoV
tTwoC = ((textTwo.consonants - tTwoC)**2)/tTwoC

chiSq = tOneV+tOneC+tTwoV+tTwoC

print(" ")
print("Chi-square is ",round(chiSq,2))

