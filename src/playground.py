from note import *


testDict = dict([])
testDict['hj'] = 19
testDict['other'] = 73

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