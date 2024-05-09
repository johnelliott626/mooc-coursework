# import modules
import csv
import sys


def main():

    # Ensure correct usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # open the csv file with DictReader and read into memory with the list people
    people = []
    filename = sys.argv[1]
    with open(filename) as file:
        reader = csv.DictReader(file)
        for row in reader:
            people.append(row)

    # open the dna sequence and read into memory
    sequenceFileName = sys.argv[2]
    with open(sequenceFileName) as sequenceFile:
        DNA = sequenceFile.read()

    # compute longest number of consecutive repeats of the STR in the DNA sequence
    keys = []

    for key in people[0].keys():
        keys.append(key)
    keys.remove('name')

    # create a dictionary of the count of each STR as the key and the value as the max count initialized to zero
    strCounts = {}
    for i in keys:
        strCounts[i] = 0

    # search the input string until the end for the max value, for each STR in keys
    for i in keys:
        strCounts[i] = getSTRMaxValue(DNA, i)

    # check if the DNA matches with anyone in the csv
    found = False
    for i in people:
        flag = True
        for j in strCounts:
            if int(strCounts[j]) != int(i[j]):
                flag = False
 
        if flag == True:
            found = True
            print(i['name'])
    
    if found == False:
        print("No match")
    

def getSTRMaxValue(inputSequence, STR):
    iterations = 0
    continueSearching = True
    currentMax = 0

    while continueSearching == True:
        returnVals = repeatedSTRS(inputSequence, STR)

        # if the STR does not appear in the sequence at all
        if returnVals == 0 and iterations == 0:
            return 0

        # if the STR does not appear in the current rest of the substring
        elif returnVals == 0:
            continueSearching = False

        # else the STR appears at least once in proceeding substring
        else:
            if returnVals[0] > currentMax:
                currentMax = returnVals[0]
            latestIndex = returnVals[1] + 1
            inputSequence = inputSequence[latestIndex:]

        iterations += 1

    return currentMax


def repeatedSTRS(inputSequence, STR):
    counter = 0
    flag = True
    STRlength = len(STR)
    jump = STRlength
    returnList = []
    STRindex = inputSequence.find(STR)

    # if that STR is not found at all in the sequence
    if STRindex == -1:
        return 0

    latestIndex = STRindex + STRlength
    counter = 1

    # counts the number of times to STR repeats sequentially
    while flag == True:
        if (inputSequence.find(STR, (STRindex + jump), (STRindex + jump + STRlength)) != -1):
            latestIndex = (STRindex + jump + STRlength)
            counter += 1
            jump = jump + STRlength
        else:
            flag = False

    returnList.append(counter)
    returnList.append(latestIndex)
    return returnList


main()
