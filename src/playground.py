from note import *
import time


testDict = dict([])
testDict['hj'] = 19
testDict['other'] = 73
print(testDict)

testList = [9,4,5,3,2]
print(testList)

for key in testDict:
    print(key)
def printOutOfScope():
    print(testVar)
print(testDict['hj'])

testNote = note(8, 'B4')
testNote2 = note(8, 'C4')
print(testNote.getNoteLength())
testNote.decrementNoteLength()
print(testNote.getNoteLength())
print(testNote.getNoteId())
print(testNote2.getNoteId())
testNote = note(4, 'Cs4')
print(testNote.getNoteId())

print(1/16)

testVar = 6
printOutOfScope()

thisList = []
thisList.append(5)

print(thisList[1])

