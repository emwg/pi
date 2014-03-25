from note import *


testDict = dict([])
testDict['hj'] = 19


print(testDict['hj'])

testNote = note(8, 'B4')
print(testNote.getNoteLength())
testNote.decrementNoteLength()
print(testNote.getNoteLength())

measure = [84,23,56,32]
for num in measure:
    print(num)