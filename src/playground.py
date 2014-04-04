from note import *
import time


testDict = dict([])
testDict['hj'] = 19
testDict['other'] = 73

testList = [9,4,5,3,2]
print(testList)

for key in testDict:
    print(key)

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

timeInSec = time.time()
count = 1
while True:
    if(timeInSec - time.time() < -1):
        print('It has been ' + str(count) + ' seconds')
        print(timeInSec)
        count += 1
        timeInSec = time.time()